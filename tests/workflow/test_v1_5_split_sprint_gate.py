from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "docs" / "v1.5.0-split-sprint-gate-report.md"
GO_NO_GO = ROOT / "docs" / "v1.5.0-split-go-no-go.md"
LANE = ROOT / "lanes" / "321_split_sprint_gate.md"

VGGT_PACK = ROOT / "split_manual" / "turingresearch-vggt-case"
EXAMPLES_PACK = ROOT / "split_manual" / "turingresearch-examples"
GIT_DRY_RUN = ROOT / "docs" / "split-repo-git-init-dry-run.md"
RELEASE_CHECKLIST = ROOT / "docs" / "split-repo-release-checklist.md"
MAIN_PATCH = ROOT / "docs" / "main-repo-post-split-patch-v2.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _combined(paths: list[Path]) -> str:
    return "\n".join(_text(path) for path in paths)


def test_v1_5_split_sprint_gate_docs_exist() -> None:
    assert REPORT.exists()
    assert GO_NO_GO.exists()
    assert LANE.exists()


def test_v1_5_split_sprint_gate_required_artifacts_exist() -> None:
    for pack in (VGGT_PACK, EXAMPLES_PACK):
        assert (pack / "README.md").exists()
        assert (pack / "CREATE_REPO_MANUALLY.md").exists()
        assert (pack / "PUSH_COMMANDS.md").exists()
        assert (pack / "SAFETY_CHECKLIST.md").exists()
        assert (pack / "GIT_INIT_DRY_RUN.md").exists()
        assert (pack / "RELEASE_CHECKLIST.md").exists()
        assert (pack / "manifest.yaml").exists()

    assert GIT_DRY_RUN.exists()
    assert RELEASE_CHECKLIST.exists()
    assert MAIN_PATCH.exists()


def test_v1_5_split_sprint_gate_records_passes() -> None:
    text = _combined([REPORT, GO_NO_GO, LANE])

    assert "GO FOR HUMAN REVIEW / NO-GO FOR AUTOMATIC SPLIT EXECUTION" in text
    assert "vggt-case manual pack pass" in text
    assert "examples manual pack pass" in text
    assert "git init dry-run pass" in text
    assert "release checklist pass" in text
    assert "main repo patch pass" in text
    assert "no fake URL" in text
    assert "no secrets" in text
    assert "no raw data" in text


def test_v1_5_split_sprint_gate_blocks_automation() -> None:
    text = _combined([REPORT, GO_NO_GO, LANE])

    assert "No GitHub repository was created." in text
    assert "No external repository was pushed." in text
    assert "No `git init` was run for split packs." in text
    assert "No release was published." in text
    assert "No real public URL was written." in text
    assert "automatic GitHub repository creation" in text
    assert "automatic external push" in text


def test_v1_5_split_sprint_gate_is_public_safe() -> None:
    paths = [
        REPORT,
        GO_NO_GO,
        LANE,
        GIT_DRY_RUN,
        RELEASE_CHECKLIST,
        MAIN_PATCH,
        VGGT_PACK / "manifest.yaml",
        EXAMPLES_PACK / "manifest.yaml",
    ]
    combined = _combined(paths)
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"

    assert old_name not in combined
    assert private_drive not in combined
    assert "D:" + "\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert ".env=" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "https://github.com/" not in combined
