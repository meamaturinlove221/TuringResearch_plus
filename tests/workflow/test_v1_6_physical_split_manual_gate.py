from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REPORT = ROOT / "docs" / "v1.6.0-physical-split-manual-gate-report.md"
GO_NO_GO = ROOT / "docs" / "v1.6.0-split-manual-go-no-go.md"
LANE = ROOT / "lanes" / "350_physical_split_manual_gate.md"

VGGT_REPORT = ROOT / "docs" / "vggt-case-repo-creation-pack-final.md"
EXAMPLES_REPORT = ROOT / "docs" / "examples-repo-creation-pack-final.md"
URL_POLICY = ROOT / "docs" / "split-repo-url-placeholder-policy.md"
MAIN_PATCH = ROOT / "docs" / "main-repo-split-link-patch-v1.6.md"

VGGT_PACK = ROOT / "split_manual" / "turingresearch-vggt-case"
EXAMPLES_PACK = ROOT / "split_manual" / "turingresearch-examples"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_v1_6_physical_split_manual_gate_docs_exist() -> None:
    for path in [REPORT, GO_NO_GO, LANE]:
        assert path.exists(), path.relative_to(ROOT).as_posix()


def test_v1_6_physical_split_manual_gate_required_inputs_exist() -> None:
    for path in [VGGT_REPORT, EXAMPLES_REPORT, URL_POLICY, MAIN_PATCH]:
        assert path.exists(), path.relative_to(ROOT).as_posix()

    for pack in [VGGT_PACK, EXAMPLES_PACK]:
        for name in [
            "README.md",
            "FINAL_CREATE_REPO.md",
            "FINAL_PUSH_COMMANDS.md",
            "FINAL_RELEASE_CHECKLIST.md",
            "FINAL_PRIVACY_CHECK.md",
            "manifest.yaml",
        ]:
            assert (pack / name).exists(), (pack / name).relative_to(ROOT).as_posix()


def test_v1_6_physical_split_manual_gate_records_passes() -> None:
    text = _combined([REPORT, GO_NO_GO, LANE])

    assert "GO FOR HUMAN REVIEW / NO-GO FOR AUTOMATIC SPLIT EXECUTION" in text
    assert "vggt-case creation pack pass" in text
    assert "examples creation pack pass" in text
    assert "URL placeholder policy pass" in text
    assert "main repo patch pass" in text
    assert "no secrets" in text
    assert "no raw data" in text
    assert "no fake URL" in text
    assert "no unsupported claims" in text


def test_v1_6_physical_split_manual_gate_blocks_automation() -> None:
    text = _combined([REPORT, GO_NO_GO, LANE])

    assert "No GitHub repository was created." in text
    assert "No external repository was pushed." in text
    assert "No `git init` was run for split packs." in text
    assert "No release was published." in text
    assert "No real public URL was written." in text
    assert "No automatic GitHub repository creation." in text
    assert "No automatic external child repository push." in text


def test_v1_6_physical_split_manual_gate_evidence_reports_pass() -> None:
    text = _combined([VGGT_REPORT, EXAMPLES_REPORT, URL_POLICY, MAIN_PATCH])

    assert "| no secrets | pass |" in text
    assert "| no raw data | pass |" in text
    assert "| no fake URL | pass |" in text
    assert "| no unsupported claims | pass |" in text
    assert "Fake GitHub URLs are not allowed." in text
    assert "planned / manual-ready" in text
    assert "main TuringResearch repository" in text


def test_v1_6_physical_split_manual_gate_is_public_safe() -> None:
    paths = [
        REPORT,
        GO_NO_GO,
        LANE,
        VGGT_REPORT,
        EXAMPLES_REPORT,
        URL_POLICY,
        MAIN_PATCH,
        VGGT_PACK / "FINAL_CREATE_REPO.md",
        VGGT_PACK / "FINAL_PUSH_COMMANDS.md",
        EXAMPLES_PACK / "FINAL_CREATE_REPO.md",
        EXAMPLES_PACK / "FINAL_PUSH_COMMANDS.md",
        VGGT_PACK / "manifest.yaml",
        EXAMPLES_PACK / "manifest.yaml",
    ]
    combined = _combined(paths)
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"
    private_win_drive = "D:" + "\\vggt"
    https_github = "https://" + "github.com/"
    http_github = "http://" + "github.com/"
    token_like = re.compile(
        r"(sk-[A-Za-z0-9_-]{8,}|"
        r"ghp_[A-Za-z0-9_]{8,}|"
        r"github_pat_[A-Za-z0-9_]{8,}|"
        r"BEGIN [A-Z ]*PRIVATE KEY)"
    )

    assert old_name not in combined
    assert private_drive not in combined
    assert private_win_drive not in combined
    assert ".env=" not in combined
    assert token_like.search(combined) is None
    assert https_github not in combined
    assert http_github not in combined
    assert "creates_github_repo: false" in combined
    assert "pushes_external_repo: false" in combined
    assert "writes_real_url: false" in combined
