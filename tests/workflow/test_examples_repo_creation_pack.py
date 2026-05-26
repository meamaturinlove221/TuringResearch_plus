from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "split_manual" / "turingresearch-examples"
REPORT = ROOT / "docs" / "examples-repo-creation-pack-final.md"
SOURCE = ROOT / "split_ready" / "turingresearch-examples"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined_pack_text() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(PACK.rglob("*"))
        if path.is_file()
    )


def test_examples_final_creation_pack_files_exist() -> None:
    required = [
        PACK / "FINAL_CREATE_REPO.md",
        PACK / "FINAL_PUSH_COMMANDS.md",
        PACK / "FINAL_RELEASE_CHECKLIST.md",
        PACK / "FINAL_PRIVACY_CHECK.md",
        REPORT,
        SOURCE / "README.md",
        SOURCE / "examples_manifest.yaml",
    ]

    for path in required:
        assert path.exists(), path.relative_to(ROOT).as_posix()


def test_examples_final_creation_pack_records_required_metadata() -> None:
    combined = "\n".join(
        [
            _text(PACK / "FINAL_CREATE_REPO.md"),
            _text(PACK / "FINAL_RELEASE_CHECKLIST.md"),
            _text(REPORT),
        ]
    )

    assert "repo name suggestion | `turingresearch-examples`" in combined
    assert "initial branch | `main`" in combined
    assert "initial commit message | `Initial public-safe examples bundle`" in combined
    assert "<approved-real-repository-url>" in combined
    assert "Manual GitHub Creation Steps" in combined
    assert "main TuringResearch repository" in combined
    assert (
        "TuringResearch main repository URL goes here after human publication approval"
        in combined
    )


def test_examples_final_creation_pack_lists_include_and_exclude_files() -> None:
    create = _text(PACK / "FINAL_CREATE_REPO.md")
    report = _text(REPORT)
    combined = create + "\n" + report

    for item in [
        "README.md",
        "QUICKSTART.md",
        "examples_manifest.yaml",
        "PRIVACY.md",
        "safety_report.md",
        ".gitignore",
    ]:
        assert item in combined

    for item in [
        "raw data",
        "private local paths",
        "API keys, tokens, credentials, or `.env` values",
        "private logs",
        "generated huge artifacts",
        "unsupported research or benchmark claims",
    ]:
        assert item in combined


def test_examples_final_push_commands_are_commented_reference_only() -> None:
    push = _text(PACK / "FINAL_PUSH_COMMANDS.md")

    assert "Status: commented reference only / not executable." in push
    assert "# git init" in push
    assert "# git push -u origin main" in push
    assert "<approved-real-repository-url>" in push
    assert "Do not run these commands automatically." in push

    for line in push.splitlines():
        assert not line.strip().startswith("git ")


def test_examples_final_creation_pack_is_public_safe() -> None:
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
    assert ".env=" not in combined
    assert token_like.search(combined) is None
    assert https_github not in combined
    assert http_github not in combined
    assert "Demo-only content." in combined
    assert "No API key or token." in combined
    assert "No raw data." in combined
    assert "No fake or placeholder URL used as a real remote." in combined
    assert "main repo linked as flagship placeholder | pass" in combined
    assert "does not prove research success" in combined
    assert "demo outputs as observed evidence" in combined


def test_examples_final_creation_report_records_gate_decision() -> None:
    report = _text(REPORT)

    assert "Status: final manual pack generated" in report
    assert "The final examples creation pack is ready for human review." in report
    assert "It is not approval to create a GitHub repository" in report
    assert "| demo only | pass |" in report
    assert "| no raw data | pass |" in report
    assert "| no private paths | pass |" in report
    assert "| no API key | pass |" in report
    assert "| no fake URL | pass |" in report
