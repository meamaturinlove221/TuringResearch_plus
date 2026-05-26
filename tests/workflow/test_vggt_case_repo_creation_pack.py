from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "split_manual" / "turingresearch-vggt-case"
REPORT = ROOT / "docs" / "vggt-case-repo-creation-pack-final.md"
SOURCE = ROOT / "split_ready" / "turingresearch-vggt-case"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined_pack_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(PACK.rglob("*"))
        if path.is_file()
    )


def test_vggt_case_final_creation_pack_files_exist() -> None:
    required = [
        PACK / "FINAL_CREATE_REPO.md",
        PACK / "FINAL_PUSH_COMMANDS.md",
        PACK / "FINAL_RELEASE_CHECKLIST.md",
        PACK / "FINAL_PRIVACY_CHECK.md",
        REPORT,
        SOURCE / "README.md",
        SOURCE / "manifest.yaml",
    ]

    for path in required:
        assert path.exists(), path.relative_to(ROOT).as_posix()


def test_vggt_case_final_creation_pack_records_required_metadata() -> None:
    combined = "\n".join(
        [
            _text(PACK / "FINAL_CREATE_REPO.md"),
            _text(PACK / "FINAL_RELEASE_CHECKLIST.md"),
            _text(REPORT),
        ]
    )

    assert "repo name suggestion | `turingresearch-vggt-case`" in combined
    assert "initial branch | `main`" in combined
    assert "initial commit message | `Initial public-safe VGGT case study`" in combined
    assert "<approved-real-repository-url>" in combined
    assert "Manual GitHub Creation Steps" in combined
    assert "main TuringResearch repository" in combined


def test_vggt_case_final_creation_pack_lists_include_and_exclude_files() -> None:
    create = _text(PACK / "FINAL_CREATE_REPO.md")
    report = _text(REPORT)
    combined = create + "\n" + report

    for item in [
        "README.md",
        "QUICKSTART.md",
        "CASE_STUDY.md",
        "CLAIM_SAFETY.md",
        "PRIVACY.md",
        "LICENSE_NOTE.md",
        "manifest.yaml",
        "safety_report.md",
        ".gitignore",
    ]:
        assert item in combined

    for item in [
        "raw data",
        "private local paths",
        "secrets, tokens, credentials, or `.env` values",
        "restricted model payloads",
        "model checkpoints",
        "generated heavy artifacts",
    ]:
        assert item in combined


def test_vggt_case_final_push_commands_are_commented_reference_only() -> None:
    push = _text(PACK / "FINAL_PUSH_COMMANDS.md")

    assert "Status: commented reference only / not executable." in push
    assert "# git init" in push
    assert "# git push -u origin main" in push
    assert "git push -u origin main" not in [
        line.strip() for line in push.splitlines()
    ]
    assert "Do not run these commands automatically." in push


def test_vggt_case_final_creation_pack_is_public_safe() -> None:
    combined = "\n".join([_combined_pack_text(), _text(REPORT)])
    private_drive = "D:" + "/vggt"
    private_win_drive = "D:" + "\\vggt"
    old_name = "Tuling" + "Research"
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
    assert token_like.search(combined) is None
    assert https_github not in combined
    assert http_github not in combined
    assert "No automatic GitHub repository creation." in combined
    assert "No automatic external push." in combined
    assert "No SparseConv3D success claim" in combined
    assert "It is not public observed result evidence" in combined


def test_vggt_case_final_creation_report_records_gate_decision() -> None:
    report = _text(REPORT)

    assert "Status: final manual pack generated" in report
    assert "The final creation pack is ready for human review." in report
    assert "It is not approval to create a GitHub repository" in report
    assert "| no secrets | pass |" in report
    assert "| no raw data | pass |" in report
    assert "| no private paths | pass |" in report
    assert "| no restricted model payloads | pass |" in report
