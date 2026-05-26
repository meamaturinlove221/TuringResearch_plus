"""Local tool wrappers for Markdown-first run dashboards."""

from __future__ import annotations

from turing_research_plus.dashboard.markdown_render import (
    render_failure_board_markdown,
    render_run_dashboard_markdown,
    render_status_board_markdown,
)
from turing_research_plus.dashboard.models import RunDashboardReport
from turing_research_plus.dashboard.run_dashboard import build_run_dashboard
from turing_research_plus.run_ingest.models import RunIngestReport


def experiment_modal_dashboard_build(report: RunIngestReport) -> RunDashboardReport:
    """Build a dashboard from an already ingested run report."""

    return build_run_dashboard(report)


__all__ = [
    "RunDashboardReport",
    "build_run_dashboard",
    "experiment_modal_dashboard_build",
    "render_failure_board_markdown",
    "render_run_dashboard_markdown",
    "render_status_board_markdown",
]
