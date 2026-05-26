from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORT_DIR = ROOT / "split_ready" / "turingresearch-vggt-case"


def _text_files() -> list[Path]:
    return sorted(path for path in EXPORT_DIR.rglob("*") if path.is_file())


def test_v1_vggt_case_final_export_required_files_exist() -> None:
    required = {
        ".gitignore",
        "README.md",
        "CASE_STUDY.md",
        "CLAIM_SAFETY.md",
        "LICENSE_NOTE.md",
        "PRIVACY.md",
        "QUICKSTART.md",
        "manifest.yaml",
        "safety_report.md",
    }

    assert EXPORT_DIR.exists()
    assert required == {path.name for path in _text_files()}


def test_v1_vggt_case_final_export_is_public_safe() -> None:
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
    assert "SparseConv3D success" in combined
    assert "Do not claim SparseConv3D success" in combined
    assert "main repository remains the flagship" in combined.lower()


def test_v1_vggt_case_final_export_manifest_records_safety_flags() -> None:
    manifest = (EXPORT_DIR / "manifest.yaml").read_text(encoding="utf-8")

    assert "ready_to_create_after_human_approval: true" in manifest
    assert "no_raw_data: true" in manifest
    assert "no_smplx_files: true" in manifest
    assert "no_private_paths: true" in manifest
    assert "no_sparseconv3d_success_claim: true" in manifest
    assert "github_repo_creation_approval_required: true" in manifest
