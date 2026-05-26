from __future__ import annotations

import pytest

from turing_research_plus.collision.models import (
    CollisionRiskLevel,
    CollisionRiskReport,
    OverlapMatrix,
    SafeClaim,
)


def test_collision_report_requires_safe_claims_to_avoid_definitive_no_collision() -> None:
    with pytest.raises(ValueError, match="definitive no collision"):
        CollisionRiskReport(
            target_project="VGGT/SMPL-X feature adapter",
            overlap_matrix=OverlapMatrix(),
            safe_claims=[
                SafeClaim(
                    text="Definitive no collision with existing papers.",
                    basis="fake fixture",
                    caveat="none",
                )
            ],
        )


def test_risk_levels_are_stable() -> None:
    assert CollisionRiskLevel.LOW == "low"
    assert CollisionRiskLevel.MEDIUM == "medium"
    assert CollisionRiskLevel.HIGH == "high"
    assert CollisionRiskLevel.UNKNOWN == "unknown"
