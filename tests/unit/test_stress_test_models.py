from __future__ import annotations

import pytest

from turing_research_plus.stress_test.models import (
    StressFinding,
    StressScenarioId,
    StressSeverity,
    StressStatus,
    StressTestReport,
)


def test_stress_test_report_requires_human_review() -> None:
    with pytest.raises(ValueError, match="requires human review"):
        StressTestReport(
            target_id="bad-report",
            findings=[],
            status=StressStatus.PASS,
            convergence_recommendation="bad",
            requires_human_review=False,
        )


def test_stress_test_report_cannot_pass_with_blockers() -> None:
    finding = StressFinding(
        scenario_id=StressScenarioId.MISSING_EVIDENCE,
        status=StressStatus.FAIL,
        severity=StressSeverity.HIGH,
        message="missing evidence",
        recommended_action="add evidence",
    )

    with pytest.raises(ValueError, match="cannot have blockers"):
        StressTestReport(
            target_id="bad-report",
            findings=[finding],
            status=StressStatus.PASS,
            blockers=["missing_evidence"],
            convergence_recommendation="bad",
        )
