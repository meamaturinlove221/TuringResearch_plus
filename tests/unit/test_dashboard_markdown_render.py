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

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)


def test_dashboard_markdown_render_preserves_boundaries() -> None:
    run_report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )
    dashboard = build_run_dashboard(run_report)

    markdown = render_run_dashboard_markdown(dashboard)
    status_board = render_status_board_markdown(dashboard)
    failure_board = render_failure_board_markdown(dashboard)

    assert "[ROUTE_EXHAUSTED]" in markdown
    assert "Dashboard did not run Modal" in markdown
    assert "Dashboard is not an experiment result" in markdown
    assert "real_backend_missing" in status_board
    assert "REAL_BACKEND_UNAVAILABLE" in failure_board
    assert "SparseConv3D success" not in markdown
