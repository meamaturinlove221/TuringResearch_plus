from __future__ import annotations

from turing_research_plus.collision.models import CollisionRiskLevel
from turing_research_plus.collision.overlap import build_overlap_matrix
from turing_research_plus.collision.risk_scoring import score_collision_risk


def test_requires_review_fixture_can_be_unknown_not_low() -> None:
    papers = [
        {
            "paper_id": "hart",
            "title": "HART requires-real-paper-review",
            "task": "human reconstruction",
            "representation": ["requires-real-paper-review"],
        }
    ]

    scores = score_collision_risk(papers, build_overlap_matrix(papers))

    assert scores[0].level in {CollisionRiskLevel.UNKNOWN, CollisionRiskLevel.MEDIUM}
    assert scores[0].requires_human_review is True


def test_hart_overlap_is_treated_conservatively() -> None:
    papers = [
        {
            "paper_id": "hart",
            "title": "HART human reconstruction",
            "task": "human reconstruction geometry",
            "representation": ["SMPL-X", "token", "adapter"],
            "evidence_refs": ["manual-note"],
        }
    ]

    scores = score_collision_risk(papers, build_overlap_matrix(papers))

    assert scores[0].level in {CollisionRiskLevel.MEDIUM, CollisionRiskLevel.HIGH}
