"""Boundary mapping for Deep Insight workflows."""

from __future__ import annotations

from turing_research_plus.insight.models import (
    BoundaryCondition,
    BoundaryConditionType,
    BoundaryMap,
    GapValidationReport,
)


def build_boundary_map(
    gap_report: GapValidationReport,
    map_id: str = "boundary-map-1",
) -> BoundaryMap:
    """Build a minimal valid/invalid condition map from validated gaps."""

    first_gap = gap_report.gaps[0]
    return BoundaryMap(
        map_id=map_id,
        topic=gap_report.topic,
        conditions=[
            BoundaryCondition(
                condition_id="boundary-valid-1",
                condition_type=BoundaryConditionType.VALID,
                description=(
                    "Findings are valid when the problem matches the surveyed "
                    f"gap context: {first_gap.description}"
                ),
                evidence=first_gap.evidence,
            ),
            BoundaryCondition(
                condition_id="boundary-invalid-1",
                condition_type=BoundaryConditionType.INVALID,
                description=(
                    "Findings are invalid when applied outside the surveyed "
                    "evidence base or without comparable data."
                ),
                evidence=first_gap.evidence,
            ),
        ],
    )
