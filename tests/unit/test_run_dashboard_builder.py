from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard.run_dashboard import build_run_dashboard
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)


def test_run_dashboard_builder_summarizes_modal_fixture() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )

    dashboard = build_run_dashboard(run_report)

    assert dashboard.run_id == "modal-sparseconv-fixture-001"
    assert dashboard.route_id == "modal_sparseconv_v0"
    assert dashboard.candidate_count == 1
    assert dashboard.best_candidate == "fallback-proxy"
    assert dashboard.backend_status == "real_backend_missing"
    assert dashboard.artifact_completeness.missing_count == 4
    assert "visual proof insufficient" in dashboard.visual_readiness
    assert dashboard.advisor_readiness == "not-ready: backend evidence missing"
    assert dashboard.experiment_executed_by_dashboard is False
