from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPLIT_READY = ROOT / "split_ready"
SPLIT_MANUAL = ROOT / "split_manual"
REPORT = ROOT / "docs" / "split-final-safety-refresh-v1.6.md"
BLOCKERS = ROOT / "docs" / "split-final-blockers.md"
POLICY = ROOT / "docs" / "physical-split-execution-policy.md"
SPLIT_GATE = ROOT / "docs" / "v1.5.0-split-sprint-gate-report.md"
FRESHNESS = ROOT / "docs" / "vggt-case-local-freshness-recheck-v1.6.md"
LANE = ROOT / "lanes" / "345_split_final_safety_refresh.md"

TEXT_SUFFIXES = {".gitignore", ".json", ".md", ".txt", ".yaml", ".yml"}
BLOCKED_PAYLOAD_SUFFIXES = {
    ".ckpt",
    ".npz",
    ".pkl",
    ".ply",
    ".pt",
    ".pth",
    ".safetensors",
    ".zip",
}


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _text_files_under(*roots: Path) -> list[Path]:
    files: list[Path] = []
    for root in roots:
        if root.is_file() and root.suffix.lower() in TEXT_SUFFIXES:
            files.append(root)
        elif root.is_dir():
            files.extend(
                item
                for item in root.rglob("*")
                if item.is_file()
                and (item.suffix.lower() in TEXT_SUFFIXES or item.name == ".gitignore")
            )
    return sorted(set(files))


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_split_final_safety_refresh_docs_exist() -> None:
    for path in [REPORT, BLOCKERS, LANE, POLICY, SPLIT_GATE, FRESHNESS]:
        assert path.exists(), _relative(path)


def test_split_final_safety_refresh_required_packs_exist() -> None:
    required = [
        SPLIT_READY / "turingresearch-vggt-case" / "README.md",
        SPLIT_READY / "turingresearch-vggt-case" / "CLAIM_SAFETY.md",
        SPLIT_READY / "turingresearch-vggt-case" / "manifest.yaml",
        SPLIT_READY / "turingresearch-examples" / "README.md",
        SPLIT_READY / "turingresearch-examples" / "examples_manifest.yaml",
        SPLIT_MANUAL / "turingresearch-vggt-case" / "README.md",
        SPLIT_MANUAL / "turingresearch-vggt-case" / "manifest.yaml",
        SPLIT_MANUAL / "turingresearch-vggt-case" / "FRESHNESS_CHECK.md",
        SPLIT_MANUAL / "turingresearch-examples" / "README.md",
        SPLIT_MANUAL / "turingresearch-examples" / "manifest.yaml",
    ]

    for path in required:
        assert path.exists(), _relative(path)


def test_split_final_safety_refresh_reports_gate_decision() -> None:
    text = _combined([REPORT, BLOCKERS, LANE])

    assert "GO FOR FINAL HUMAN REVIEW / NO-GO FOR AUTOMATIC SPLIT EXECUTION" in text
    assert "| no secrets | pass |" in text
    assert "| no raw data | pass |" in text
    assert "| no private paths | pass |" in text
    assert "| no SMPL-X payload | pass |" in text
    assert "| no fake URL | pass |" in text
    assert "| no unsupported claims | pass |" in text
    assert "| main repo remains flagship | pass |" in text


def test_split_final_safety_refresh_blocks_automation() -> None:
    text = _combined([REPORT, BLOCKERS, LANE, POLICY, SPLIT_GATE])

    assert "No external repository was created." in text
    assert "No external child repository was pushed." in text
    assert "No `git init` was run" in text
    assert "No real URL was written." in text
    assert "automatic GitHub repository creation" in text
    assert "automatic external push" in text


def test_split_final_safety_refresh_no_secret_or_private_path_text() -> None:
    combined = _combined(_text_files_under(SPLIT_READY, SPLIT_MANUAL))
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"
    private_win_drive = "D:" + "\\vggt"
    private_path_like = re.compile(
        rf"([A-Za-z]:\\Users\\[^\\\s<]+|/home/[^/\s<]+|"
        rf"{re.escape(private_drive)}|{re.escape(private_win_drive)})"
    )
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|ghp_[A-Za-z0-9_]{8,}|"
        r"github_pat_[A-Za-z0-9_]{8,}|BEGIN [A-Z ]*PRIVATE KEY)"
    )
    assignment_like = re.compile(
        r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret|password)"
        r"\s*[:=]\s*['\"]?[A-Za-z0-9][A-Za-z0-9_-]{11,}"
    )

    assert old_name not in combined
    assert private_path_like.search(combined) is None
    assert token_like.search(combined) is None
    assert assignment_like.search(combined) is None
    assert "password=" not in combined.lower()


def test_split_final_safety_refresh_no_raw_data_or_payload_files() -> None:
    offenders: list[str] = []
    blocked_path_parts = {
        ".env",
        "local_project_links.yaml",
        "private_data",
        "raw",
        "raw_data",
    }

    for root in [SPLIT_READY, SPLIT_MANUAL]:
        for path in root.rglob("*"):
            lowered_parts = {part.lower() for part in path.parts}
            if blocked_path_parts.intersection(lowered_parts):
                offenders.append(_relative(path))
            if path.is_file() and path.suffix.lower() in BLOCKED_PAYLOAD_SUFFIXES:
                offenders.append(_relative(path))
            if path.name.startswith("SMPL" + "-X") or path.name.startswith("SMPLX_"):
                offenders.append(_relative(path))

    assert offenders == []


def test_split_final_safety_refresh_no_fake_urls() -> None:
    combined = _combined(_text_files_under(SPLIT_READY, SPLIT_MANUAL))

    assert "https://" not in combined
    assert "http://" not in combined
    assert "example.com" not in combined
    assert "deployed at" not in combined.lower()
    assert "live URL:" not in combined
    assert "<approved-real-repository-url>" in combined


def test_split_final_safety_refresh_keeps_claims_review_gated() -> None:
    combined = _combined(
        _text_files_under(
            SPLIT_READY / "turingresearch-vggt-case",
            SPLIT_MANUAL / "turingresearch-vggt-case",
            REPORT,
            BLOCKERS,
            FRESHNESS,
        )
    )
    forbidden_claims = [
        "SparseConv3D success | observed",
        "SparseConv3D success | local-observed",
        "SparseConv3D succeeded",
        "SparseConv3D is successful",
        "VGGT experiment succeeded",
        "advisor approval | observed",
        "public release readiness | observed",
    ]

    for phrase in forbidden_claims:
        assert phrase not in combined

    assert "SparseConv3D success | requires-human-review" in combined
    assert "No SparseConv3D success claim" in combined
    assert "not proof that any VGGT or SparseConv3D experiment succeeded" in combined
    assert "Local metadata is not public observed result evidence." in combined


def test_split_final_safety_refresh_flagship_remains_canonical() -> None:
    combined = _combined(
        _text_files_under(SPLIT_READY, SPLIT_MANUAL)
        + [REPORT, BLOCKERS, POLICY, SPLIT_GATE]
    )

    assert "main_repo_remains_flagship: true" in combined
    assert "main TuringResearch repository remains the flagship" in combined
    assert "The flagship TuringResearch repository remains the source of truth." in combined
    assert "main TuringResearch repository remains the flagship install" in combined
