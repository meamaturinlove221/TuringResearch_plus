from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


V0_4_CONTRACTS = [
    "github_artifact_sync.yaml",
    "ssh_sftp_remote_reader.yaml",
    "nas_smb_shared_store.yaml",
    "cloud_object_artifact_index.yaml",
    "remote_artifacts.yaml",
    "modal_run_dashboard.yaml",
    "run_comparison.yaml",
    "paper_digest.yaml",
    "advisor_export.yaml",
]


def test_v0_4_contracts_exist() -> None:
    missing = [name for name in V0_4_CONTRACTS if not (ROOT / "contracts" / name).exists()]

    assert missing == []


def test_v0_4_contracts_are_review_first_and_no_default_network() -> None:
    offenders: list[str] = []
    for name in V0_4_CONTRACTS:
        text = (ROOT / "contracts" / name).read_text(encoding="utf-8")
        lowered = text.lower()
        if "TuringResearch Plus" not in text:
            offenders.append(f"{name} missing project name")
        no_network_boundary = any(
            marker in lowered
            for marker in [
                "no_network",
                "no_default_network",
                "fake_mode_default",
                "local_mounted_path_only",
                "default tests must not access network",
            ]
        )
        if not no_network_boundary:
            offenders.append(f"{name} missing no-network boundary")
        review_boundary = any(
            marker in lowered
            for marker in [
                "requires_human_review",
                "human_review_required",
                "requires human review",
                "retrieved, not verified",
                "not human verified",
            ]
        )
        if not review_boundary:
            offenders.append(f"{name} missing human review boundary")

    assert offenders == []


def test_v0_4_docs_and_examples_exist() -> None:
    required = [
        ROOT / "docs" / "remote-artifact-integration.md",
        ROOT / "docs" / "modal-run-dashboard.md",
        ROOT / "docs" / "run-comparison.md",
        ROOT / "docs" / "paper-digest-engine.md",
        ROOT / "docs" / "advisor-export-plan.md",
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "advisor_export"
        / "manifest.yaml",
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "paper_digest"
        / "humanram_digest.fixture.md",
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "run_comparison"
        / "vggt_run_comparison.md",
    ]

    assert [path for path in required if not path.exists()] == []


def test_v0_4_release_boundaries_are_documented() -> None:
    advisor_manifest = (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "advisor_export"
        / "manifest.yaml"
    ).read_text(encoding="utf-8")
    run_comparison = (
        ROOT
        / "examples"
        / "vggt-human-prior-survey"
        / "run_comparison"
        / "vggt_run_comparison.md"
    ).read_text(encoding="utf-8")

    assert "generated_binary_exports: false" in advisor_manifest
    assert "no_pdf_generated" in advisor_manifest
    assert "no_pptx_generated" in advisor_manifest
    assert "SparseConv3D success requires real backend evidence" in run_comparison
    assert "No Modal or VGGT execution was performed" in run_comparison
