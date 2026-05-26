"""Local helper wrappers for run comparison."""

from __future__ import annotations

from turing_research_plus.dashboard.models import RunDashboardReport
from turing_research_plus.run_compare.comparator import compare_runs, input_from_dashboard
from turing_research_plus.run_compare.models import RunComparisonInput, RunComparisonReport


def experiment_run_compare(runs: list[RunComparisonInput]) -> RunComparisonReport:
    """Build a metadata-only run comparison report."""

    return compare_runs(runs)


def experiment_run_compare_from_dashboards(
    dashboards: list[RunDashboardReport],
) -> RunComparisonReport:
    """Build a comparison report from dashboard reports."""

    return compare_runs([input_from_dashboard(report) for report in dashboards])
