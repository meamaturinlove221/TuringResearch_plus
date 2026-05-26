from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPLIT_READY = ROOT / "split_ready"
VGGT_CASE = SPLIT_READY / "turingresearch-vggt-case"
EXAMPLES = SPLIT_READY / "turingresearch-examples"


def _combined_text(path: Path) -> str:
    return "\n".join(
        item.read_text(encoding="utf-8")
        for item in sorted(path.rglob("*"))
        if item.is_file()
    )


def test_v1_1_vggt_case_bundle_is_ready_for_human_creation() -> None:
    required = {
        ".gitignore",
        "CASE_STUDY.md",
        "CLAIM_SAFETY.md",
        "LICENSE_NOTE.md",
        "PRIVACY.md",
        "QUICKSTART.md",
        "README.md",
        "manifest.yaml",
        "safety_report.md",
    }

    assert VGGT_CASE.exists()
    assert required == {item.name for item in VGGT_CASE.iterdir() if item.is_file()}

    manifest = (VGGT_CASE / "manifest.yaml").read_text(encoding="utf-8")
    readme = (VGGT_CASE / "README.md").read_text(encoding="utf-8")

    assert "ready_to_create_after_human_approval: true" in manifest
    assert "creates_github_repo: false" in manifest
    assert "pushes_git: false" in manifest
    assert "not yet a GitHub repository" in readme
    assert "main TuringResearch repository remains the flagship" in readme


def test_v1_1_examples_bundle_is_ready_for_human_creation() -> None:
    required = {
        ".gitignore",
        "PRIVACY.md",
        "QUICKSTART.md",
        "README.md",
        "examples_manifest.yaml",
        "safety_report.md",
    }

    assert EXAMPLES.exists()
    assert required == {item.name for item in EXAMPLES.iterdir() if item.is_file()}

    manifest = (EXAMPLES / "examples_manifest.yaml").read_text(encoding="utf-8")
    readme = (EXAMPLES / "README.md").read_text(encoding="utf-8")

    assert "ready_to_create_after_human_approval: true" in manifest
    assert "creates_github_repo: false" in manifest
    assert "pushes_git: false" in manifest
    assert "not yet a GitHub repository" in readme
    assert "flagship TuringResearch repository remains" in readme


def test_v1_1_split_ready_bundles_are_public_safe() -> None:
    combined = "\n".join(
        [
            _combined_text(VGGT_CASE),
            _combined_text(EXAMPLES),
            (SPLIT_READY / "split_manifest.yaml").read_text(encoding="utf-8"),
        ]
    )
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
    assert "fake_demo_as_observed: true" in combined
    assert "not a sparseconv3d success claim" in combined.lower()
    assert "Demo output is not research success evidence" in combined


def test_v1_1_split_manifest_preserves_star_strategy_and_deferrals() -> None:
    manifest = (SPLIT_READY / "split_manifest.yaml").read_text(encoding="utf-8")

    assert "source_of_truth: flagship" in manifest
    assert "github_repo_creation: false" in manifest
    assert "external_push: false" in manifest
    assert "repo_id: turingresearch-vggt-case" in manifest
    assert "repo_id: turingresearch-examples" in manifest
    assert "status: ready-after-human-approval" in manifest
    assert "repo_id: turingresearch-plugins" in manifest
    assert "status: deferred-until-ecosystem-demand" in manifest
    assert "no_core_features_in_spokes: true" in manifest


def test_v1_1_split_readme_does_not_use_fake_external_urls() -> None:
    combined = "\n".join(
        [
            (VGGT_CASE / "README.md").read_text(encoding="utf-8"),
            (EXAMPLES / "README.md").read_text(encoding="utf-8"),
        ]
    )

    assert "https://github.com/" not in combined
    assert "Flagship placeholder" in combined
    assert "Please use and star" in combined
