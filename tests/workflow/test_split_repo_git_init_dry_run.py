from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "split_manual" / "turingresearch-vggt-case" / "GIT_INIT_DRY_RUN.md"
EXAMPLES = ROOT / "split_manual" / "turingresearch-examples" / "GIT_INIT_DRY_RUN.md"
REPORT = ROOT / "docs" / "split-repo-git-init-dry-run.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_split_repo_git_init_dry_run_files_exist() -> None:
    assert VGGT.exists()
    assert EXAMPLES.exists()
    assert REPORT.exists()


def test_vggt_case_git_init_dry_run_is_reference_only() -> None:
    text = _text(VGGT)

    assert "Status: dry-run only." in text
    assert "It does not run `git" in text
    assert "# git init" in text
    assert "# git push -u origin main" in text
    assert "<approved-real-repository-url>" in text
    assert "Initial public-safe VGGT case study" in text
    assert "main" in text
    assert "Do not claim VGGT or SparseConv3D success." in text


def test_examples_git_init_dry_run_is_reference_only() -> None:
    text = _text(EXAMPLES)

    assert "Status: dry-run only." in text
    assert "It does not run `git init`" in text
    assert "# git init" in text
    assert "# git push -u origin main" in text
    assert "<approved-real-repository-url>" in text
    assert "Initial public-safe examples bundle" in text
    assert "main" in text
    assert "Do not include raw data, API keys, private paths, or huge artifacts." in text


def test_split_repo_git_init_dry_run_report_records_non_actions() -> None:
    text = _text(REPORT)

    assert "No `git init` was executed." in text
    assert "No `.git/` directory was created in split manual packs." in text
    assert "No GitHub repository was created." in text
    assert "No external remote was configured." in text
    assert "No external push was performed." in text
    assert "No real public URL was written." in text


def test_split_repo_git_init_dry_run_is_public_safe() -> None:
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
    assert "<approved-real-repository-url>" in combined
