"""Sensitivity probing for Deep Insight workflows."""

from __future__ import annotations

from turing_research_plus.insight.models import (
    AssumptionSensitivity,
    GapValidationReport,
    SensitivityReport,
)


def probe_sensitivity(
    gap_report: GapValidationReport,
    report_id: str = "sensitivity-report-1",
) -> SensitivityReport:
    """Identify load-bearing assumptions from validated gaps."""

    first_gap = gap_report.gaps[0]
    assumptions = [
        AssumptionSensitivity(
            assumption_id="assumption-1",
            statement="The surveyed evidence base is representative enough to guide synthesis.",
            load_bearing=True,
            sensitivity="If false, gap priority and downstream insights must be revisited.",
            evidence=first_gap.evidence,
        ),
        AssumptionSensitivity(
            assumption_id="assumption-2",
            statement="Terminology is comparable across included studies.",
            load_bearing=False,
            sensitivity=(
                "If false, taxonomy labels need normalization before implementation planning."
            ),
            evidence=first_gap.evidence,
        ),
    ]
    return SensitivityReport(
        report_id=report_id,
        topic=gap_report.topic,
        assumptions=assumptions,
    )
