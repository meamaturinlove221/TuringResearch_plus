from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
FUTURE = ROOT / "docs" / "future-split-repos.md"
READY = ROOT / "docs" / "split-ready-bundles.md"
MANUAL = ROOT / "docs" / "split-manual-packs.md"
PATCH = ROOT / "docs" / "main-repo-post-split-patch-v2.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_main_repo_post_split_patch_docs_exist() -> None:
    assert README.exists()
    assert FUTURE.exists()
    assert READY.exists()
    assert MANUAL.exists()
    assert PATCH.exists()


def test_readme_uses_manual_ready_without_fake_urls() -> None:
    text = _text(README)

    assert "planned / manual-ready" in text
    assert "split_manual/" in text
    assert "The main TuringResearch repository remains the only install" in text
    assert "star entry" in text
    assert "https://github.com/" not in text


def test_split_docs_preserve_flagship_install_and_star() -> None:
    combined = "\n".join([_text(FUTURE), _text(READY), _text(MANUAL), _text(PATCH)])

    assert "planned / manual-ready" in combined
    assert "no fake URL" in combined
    assert "The main repository remains the install entry." in combined
    assert "Child repositories are case/demo spokes only." in combined
    assert "star target" in combined
    assert "split_ready/" in combined
    assert "split_manual/" in combined


def test_post_split_patch_v2_is_public_safe() -> None:
    combined = "\n".join([_text(README), _text(FUTURE), _text(READY), _text(MANUAL), _text(PATCH)])
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"

    assert old_name not in combined
    assert private_drive not in combined
    assert "D:" + "\\vggt" not in combined
    assert "local_project_links.yaml" not in combined
    assert ".env=" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
