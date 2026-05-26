"""Status badge helpers for run dashboards."""

from __future__ import annotations

from turing_research_plus.dashboard.models import DashboardBadge
from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.models import BackendStatus, RunIngestReport, RunStatus

BADGE_LABELS: dict[DashboardBadge, str] = {
    DashboardBadge.REVIEW_READY_NOT_PROMOTED: "[REVIEW_READY_NOT_PROMOTED]",
    DashboardBadge.HARD_BLOCKED: "[HARD_BLOCKED]",
    DashboardBadge.ROUTE_EXHAUSTED: "[ROUTE_EXHAUSTED]",
    DashboardBadge.FAILED: "[FAILED]",
    DashboardBadge.PARTIAL: "[PARTIAL]",
    DashboardBadge.NOT_ENOUGH_EVIDENCE: "[NOT_ENOUGH_EVIDENCE]",
    DashboardBadge.REQUIRES_HUMAN_REVIEW: "[REQUIRES_HUMAN_REVIEW]",
}


def badges_for_run(report: RunIngestReport) -> list[DashboardBadge]:
    """Return stable badges for a run ingest report."""

    badges: list[DashboardBadge] = []
    if report.status == RunStatus.REVIEW_READY_NOT_PROMOTED:
        badges.append(DashboardBadge.REVIEW_READY_NOT_PROMOTED)
    if report.status == RunStatus.HARD_BLOCKED:
        badges.append(DashboardBadge.HARD_BLOCKED)
    if report.status == RunStatus.ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS:
        badges.append(DashboardBadge.ROUTE_EXHAUSTED)
    if report.status == RunStatus.RUN_FAILED:
        badges.append(DashboardBadge.FAILED)
    if report.status == RunStatus.PARTIAL:
        badges.append(DashboardBadge.PARTIAL)
    if (
        FailureCategory.NOT_ENOUGH_EVIDENCE in report.failure_categories
        or report.backend_status != BackendStatus.REAL_BACKEND_CONFIRMED
        or report.missing_artifacts
    ):
        badges.append(DashboardBadge.NOT_ENOUGH_EVIDENCE)
    if report.requires_human_review:
        badges.append(DashboardBadge.REQUIRES_HUMAN_REVIEW)
    return list(dict.fromkeys(badges))


def badge_label(badge: DashboardBadge) -> str:
    """Return a Markdown-safe badge label."""

    return BADGE_LABELS[badge]
