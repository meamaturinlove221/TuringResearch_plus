from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPLAY = ROOT / "examples" / "vggt-human-prior-survey" / "dogfooding_replay"


def test_vggt_dogfooding_replay_files_exist() -> None:
    required = [
        "replay_report.md",
        "replay_manifest.yaml",
        "replay_missing_items.md",
        "replay_next_actions.md",
    ]

    for filename in required:
        assert (REPLAY / filename).exists()


def test_vggt_dogfooding_replay_manifest_preserves_boundaries() -> None:
    manifest = (REPLAY / "replay_manifest.yaml").read_text(encoding="utf-8")

    assert "status: replay-only" in manifest
    assert "network_used: false" in manifest
    assert "vggt_experiment_run: false" in manifest
    assert "modal_run: false" in manifest
    assert "private_vggt_path_read: false" in manifest
    assert "generated_new_results: false" in manifest
    assert "sparseconv3d_success_claimed: false" in manifest


def test_vggt_dogfooding_replay_chain_is_complete() -> None:
    report = (REPLAY / "replay_report.md").read_text(encoding="utf-8")
    required_steps = [
        "research intent",
        "evidence ledger",
        "artifact audit",
        "visual audit",
        "run ingest",
        "failure taxonomy",
        "route DSL",
        "related work",
        "vault graph",
        "advisor pack",
        "dashboard",
        "next action",
    ]

    for step in required_steps:
        assert step in report


def test_vggt_dogfooding_replay_uses_required_status_labels() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in REPLAY.glob("*.*"))

    for label in [
        "observed",
        "planned",
        "missing",
        "not-enough-evidence",
        "requires-human-review",
    ]:
        assert label in combined


def test_vggt_dogfooding_replay_does_not_claim_sparseconv_success() -> None:
    report = (REPLAY / "replay_report.md").read_text(encoding="utf-8")
    manifest = (REPLAY / "replay_manifest.yaml").read_text(encoding="utf-8")
    next_actions = (REPLAY / "replay_next_actions.md").read_text(encoding="utf-8")

    assert "SparseConv3D success is not established" in report
    assert "sparseconv3d_success_claimed: false" in manifest
    assert "Do not state that VGGT, Modal, or SparseConv3D succeeded" in next_actions


def test_vggt_dogfooding_replay_missing_items_are_not_observed() -> None:
    missing = (REPLAY / "replay_missing_items.md").read_text(encoding="utf-8")

    assert "Missing is not observed" in missing
    assert "Planned is not executed" in missing
    assert "real sparse backend probe log" in missing
    assert "predictions.npz" in missing
