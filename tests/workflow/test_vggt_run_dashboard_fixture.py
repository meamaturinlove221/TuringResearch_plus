from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard.markdown_render import (
    render_failure_board_markdown,
    render_run_dashboard_markdown,
    render_status_board_markdown,
)
from turing_research_plus.dashboard.run_dashboard import build_run_dashboard
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)
EXAMPLE_DASHBOARD = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "dashboard"
    / "run_dashboard.md"
)


def test_vggt_run_dashboard_fixture_is_review_only() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )
    dashboard = build_run_dashboard(run_report)

    assert dashboard.run_status == "ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS"
    assert dashboard.backend_status == "real_backend_missing"
    assert dashboard.artifact_completeness.missing_artifacts == [
        "predictions.npz",
        "board_inventory.md",
        "sha256_manifest.txt",
        "cleanup_report.md",
    ]
    assert "REAL_BACKEND_UNAVAILABLE" in dashboard.failure_categories
    assert dashboard.experiment_executed_by_dashboard is False


def test_vggt_run_dashboard_example_matches_runtime_boundaries() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )
    dashboard = build_run_dashboard(run_report)

    generated = render_run_dashboard_markdown(dashboard)
    existing = EXAMPLE_DASHBOARD.read_text(encoding="utf-8")

    assert "Dashboard did not run Modal" in generated
    assert "Dashboard did not run Modal" in existing
    assert "SparseConv3D success" not in generated
    assert "SparseConv3D success" not in existing
    assert "[NOT_ENOUGH_EVIDENCE]" in render_status_board_markdown(dashboard)
    assert "VISUAL_PROOF_INSUFFICIENT" in render_failure_board_markdown(dashboard)
