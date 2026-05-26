"""Build run dashboards from RunIngestReport objects."""

from __future__ import annotations

from turing_research_plus.dashboard.models import (
    DashboardArtifactCompleteness,
    DashboardGateView,
    RunDashboardReport,
)
from turing_research_plus.dashboard.status_badges import badges_for_run
from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.run_ingest.models import BackendStatus, RunIngestReport


def build_run_dashboard(report: RunIngestReport) -> RunDashboardReport:
    """Build a Markdown-first dashboard from an ingested run report."""

    present_count = len([artifact for artifact in report.artifacts if artifact.present])
    missing_count = len(report.missing_artifacts)
    best_candidate = (
        report.best_candidate.candidate_id if report.best_candidate is not None else None
    )
    return RunDashboardReport(
        run_id=report.run_id,
        route_id=report.route_id,
        run_status=report.status.value,
        status_badges=badges_for_run(report),
        candidate_count=len(report.candidates),
        best_candidate=best_candidate,
        backend_status=report.backend_status.value,
        hard_gates=[
            DashboardGateView(
                gate_id=gate.gate_id,
                passed=gate.passed,
                reason=gate.reason,
            )
            for gate in report.hard_gate_results
        ],
        artifact_completeness=DashboardArtifactCompleteness(
            present_count=present_count,
            missing_count=missing_count,
            missing_artifacts=report.missing_artifacts,
        ),
        visual_readiness=_visual_readiness(report),
        failure_categories=[category.value for category in report.failure_categories],
        next_action=_next_action(report),
        advisor_readiness=_advisor_readiness(report),
        source_report=report.source_path,
        requires_human_review=True,
        experiment_executed_by_dashboard=False,
        human_verified=False,
        limitations=[
            "Dashboard displays Run Ingestor output only.",
            "Dashboard does not run Modal or VGGT.",
            "Dashboard is not an experiment result or evidence promotion.",
        ],
    )


def _visual_readiness(report: RunIngestReport) -> str:
    if FailureCategory.VISUAL_PROOF_INSUFFICIENT in report.failure_categories:
        return "blocked: visual proof insufficient"
    if "board_inventory.md" in report.missing_artifacts:
        return "blocked: board inventory missing"
    return "review-required"


def _advisor_readiness(report: RunIngestReport) -> str:
    if report.backend_status != BackendStatus.REAL_BACKEND_CONFIRMED:
        return "not-ready: backend evidence missing"
    if report.missing_artifacts:
        return "not-ready: required artifacts missing"
    return "review-ready-not-promoted"


def _next_action(report: RunIngestReport) -> str:
    if report.backend_status != BackendStatus.REAL_BACKEND_CONFIRMED:
        return "collect real sparse backend log before making success claims"
    if report.missing_artifacts:
        return "complete missing artifacts and rerun hard gate validation"
    return "review advisor pack inputs before promotion"
