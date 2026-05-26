"""Markdown rendering for run dashboards."""

from __future__ import annotations

from turing_research_plus.dashboard.models import RunDashboardReport
from turing_research_plus.dashboard.status_badges import badge_label


def render_run_dashboard_markdown(report: RunDashboardReport) -> str:
    """Render the full dashboard Markdown."""

    lines = [
        f"# Run Dashboard: {report.run_id}",
        "",
        " ".join(badge_label(badge) for badge in report.status_badges),
        "",
        f"- Route id: `{report.route_id}`",
        f"- Run status: `{report.run_status}`",
        f"- Backend status: `{report.backend_status}`",
        f"- Candidate count: `{report.candidate_count}`",
        f"- Best candidate: `{report.best_candidate or 'none'}`",
        f"- Visual readiness: `{report.visual_readiness}`",
        f"- Advisor readiness: `{report.advisor_readiness}`",
        f"- Next action: {report.next_action}",
        "",
        "## Hard Gates",
        "",
        *[
            f"- [{'x' if gate.passed else ' '}] `{gate.gate_id}` - {gate.reason}"
            for gate in report.hard_gates
        ],
        "",
        "## Artifact Completeness",
        "",
        f"- Present: `{report.artifact_completeness.present_count}`",
        f"- Missing: `{report.artifact_completeness.missing_count}`",
        "",
        *[
            f"- missing `{artifact}`"
            for artifact in report.artifact_completeness.missing_artifacts
        ],
        "",
        "## Failure Categories",
        "",
        *[f"- `{category}`" for category in report.failure_categories],
        "",
        "## Boundary",
        "",
        "- Dashboard did not run Modal.",
        "- Dashboard did not run VGGT.",
        "- Dashboard displays already ingested evidence only.",
        "- Dashboard is not an experiment result.",
        "",
    ]
    return "\n".join(lines)


def render_status_board_markdown(report: RunDashboardReport) -> str:
    """Render a compact status board."""

    lines = [
        f"# Status Board: {report.run_id}",
        "",
        f"- Status: `{report.run_status}`",
        f"- Backend: `{report.backend_status}`",
        f"- Advisor readiness: `{report.advisor_readiness}`",
        f"- Visual readiness: `{report.visual_readiness}`",
        f"- Badges: {' '.join(badge_label(badge) for badge in report.status_badges)}",
        "",
    ]
    return "\n".join(lines)


def render_failure_board_markdown(report: RunDashboardReport) -> str:
    """Render a compact failure board."""

    lines = [
        f"# Failure Board: {report.run_id}",
        "",
        "## Failure Categories",
        "",
        *[f"- `{category}`" for category in report.failure_categories],
        "",
        "## Next Action",
        "",
        report.next_action,
        "",
    ]
    return "\n".join(lines)
