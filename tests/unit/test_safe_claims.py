from __future__ import annotations

from turing_research_plus.collision.models import CollisionRiskLevel, RiskScore
from turing_research_plus.collision.safe_claims import build_safe_claims, build_unsafe_claims


def test_safe_claims_are_conservative() -> None:
    claims = build_safe_claims(
        [
            RiskScore(
                paper_id="p",
                title="Paper",
                level=CollisionRiskLevel.UNKNOWN,
                score=0.4,
                rationale="fixture requires review",
            )
        ]
    )

    assert all("definitive no collision" not in claim.text.lower() for claim in claims)
    assert any("does not prove novelty" in claim.caveat.lower() for claim in claims)


def test_unsafe_claims_explain_why_claim_is_unsafe() -> None:
    claims = build_unsafe_claims(
        [
            RiskScore(
                paper_id="p",
                title="Paper",
                level=CollisionRiskLevel.UNKNOWN,
                score=0.4,
                rationale="fixture requires review",
            )
        ]
    )

    assert any("definitively no collision" in claim.text.lower() for claim in claims)
    assert all(claim.reason for claim in claims)
