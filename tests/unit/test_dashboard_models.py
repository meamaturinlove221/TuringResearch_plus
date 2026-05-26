from __future__ import annotations

import pytest

from turing_research_plus.dashboard.models import (
    DashboardArtifactCompleteness,
    RunDashboardReport,
)


def test_dashboard_report_serializes() -> None:
    report = RunDashboardReport(
        run_id="run-1",
        route_id="route-1",
        run_status="PARTIAL",
        candidate_count=0,
        backend_status="unknown",
        artifact_completeness=DashboardArtifactCompleteness(
            present_count=0,
            missing_count=1,
            missing_artifacts=["predictions.npz"],
        ),
        visual_readiness="blocked",
        failure_categories=["NOT_ENOUGH_EVIDENCE"],
        next_action="collect evidence",
        advisor_readiness="not-ready",
    )

    payload = report.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["experiment_executed_by_dashboard"] is False
    assert payload["human_verified"] is False


def test_dashboard_report_cannot_claim_execution() -> None:
    with pytest.raises(ValueError, match="must not claim experiment execution"):
        RunDashboardReport(
            run_id="run-1",
            route_id="route-1",
            run_status="PARTIAL",
            candidate_count=0,
            backend_status="unknown",
            artifact_completeness=DashboardArtifactCompleteness(
                present_count=0,
                missing_count=0,
            ),
            visual_readiness="review-required",
            failure_categories=[],
            next_action="review",
            advisor_readiness="review-required",
            experiment_executed_by_dashboard=True,
        )
