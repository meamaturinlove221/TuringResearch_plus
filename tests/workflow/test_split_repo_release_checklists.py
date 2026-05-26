from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "split_manual" / "turingresearch-vggt-case" / "RELEASE_CHECKLIST.md"
EXAMPLES = ROOT / "split_manual" / "turingresearch-examples" / "RELEASE_CHECKLIST.md"
REPORT = ROOT / "docs" / "split-repo-release-checklist.md"

REQUIRED_ITEMS = [
    "repo created manually",
    "README reviewed",
    "license reviewed",
    "privacy reviewed",
    "no secrets",
    "no raw data",
    "no private paths",
    "main repo linked",
    "first release draft",
    "issue templates optional",
]


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_split_repo_release_checklists_exist() -> None:
    assert VGGT.exists()
    assert EXAMPLES.exists()
    assert REPORT.exists()


def test_vggt_case_release_checklist_has_required_items() -> None:
    text = _text(VGGT)

    for item in REQUIRED_ITEMS:
        assert item in text

    assert "not released" in text
    assert "No VGGT experiment success claim is present." in text
    assert "No SparseConv3D success claim is present." in text
    assert "main TuringResearch" in text


def test_examples_release_checklist_has_required_items() -> None:
    text = _text(EXAMPLES)

    for item in REQUIRED_ITEMS:
        assert item in text

    assert "not released" in text
    assert "Content is demo-only." in text
    assert "No API key or token is present." in text
    assert "No huge artifact is present." in text
    assert "main TuringResearch" in text


def test_split_repo_release_report_records_non_actions() -> None:
    text = _text(REPORT)

    assert "Status: checklist prepared / not released." in text
    assert "No release was published." in text
    assert "No tag was created." in text
    assert "No GitHub repository was created." in text
    assert "No external remote was pushed." in text
    assert "No real public URL was written." in text


def test_split_repo_release_checklists_are_public_safe() -> None:
    combined = "\n".join([_text(VGGT), _text(EXAMPLES), _text(REPORT)])
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"

    assert old_name not in combined
    assert private_drive not in combined
    assert "D:" + "\\vggt" not in combined
    assert ".env=" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "https://github.com/" not in combined
