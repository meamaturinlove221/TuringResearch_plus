from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = ROOT / "split_ready" / "turingresearch-examples"


def _text_files() -> list[Path]:
    return sorted(path for path in EXPORT_DIR.rglob("*") if path.is_file())


def test_v1_examples_final_export_required_files_exist() -> None:
    required = {
        ".gitignore",
        "PRIVACY.md",
        "QUICKSTART.md",
        "README.md",
        "examples_manifest.yaml",
        "safety_report.md",
    }

    assert EXPORT_DIR.exists()
    assert required == {path.name for path in _text_files()}


def test_v1_examples_final_export_is_public_safe() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in _text_files())
    old_name = "Tuling" + "Research"
    private_drive = "D:" + "/vggt"
    smplx_payload = "SMPL" + "X_"

    assert old_name not in combined
    assert private_drive not in combined
    assert "D:" + "\\vggt" not in combined
    assert ".env=" not in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert smplx_payload not in combined
    assert "demo output is not research success evidence" in combined.lower()
    assert "flagship TuringResearch repository remains" in combined


def test_v1_examples_final_export_manifest_records_safety_flags() -> None:
    manifest = (EXPORT_DIR / "examples_manifest.yaml").read_text(encoding="utf-8")

    assert "ready_to_create_after_human_approval: true" in manifest
    assert "examples_are_fake_demo_by_default: true" in manifest
    assert "raw_data: true" in manifest
    assert "api_keys: true" in manifest
    assert "huge_artifacts: true" in manifest
    assert "main_repo_remains_flagship: true" in manifest
    assert "no_github_repo_creation_without_approval: true" in manifest
