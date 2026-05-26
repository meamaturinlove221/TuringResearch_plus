"""Safe and unsafe claim generation."""

from __future__ import annotations

from turing_research_plus.collision.models import (
    CollisionRiskLevel,
    RiskScore,
    SafeClaim,
    UnsafeClaim,
)


def build_safe_claims(risk_scores: list[RiskScore]) -> list[SafeClaim]:
    """Build conservative safe claims."""

    claims = [
        SafeClaim(
            text="The current VGGT direction should be described as SMPL-X feature encoding.",
            basis="Sprint documents and route pack define feature encoding as the north star.",
            caveat="This does not prove novelty or absence of collision.",
        ),
        SafeClaim(
            text="NeuralBody and HumanRAM can be used as comparison lenses.",
            basis="Fixture method cards mark related representations and human-prior usage.",
            caveat="Fixtures require real paper review before final related-work claims.",
        ),
    ]
    needs_review = any(
        score.level in {CollisionRiskLevel.HIGH, CollisionRiskLevel.UNKNOWN}
        for score in risk_scores
    )
    if needs_review:
        claims.append(
            SafeClaim(
                text="Some related work requires focused manual review before strong positioning.",
                basis="Risk scores include high or unknown levels.",
                caveat="Do not claim final collision status yet.",
            )
        )
    return claims


def build_unsafe_claims(risk_scores: list[RiskScore]) -> list[UnsafeClaim]:
    """Build claims that are unsafe under fixture evidence."""

    claims = [
        UnsafeClaim(
            text="There is definitively no collision with existing papers.",
            reason="Fake/manual method cards and fake citation graph are not sufficient evidence.",
        ),
        UnsafeClaim(
            text="The related work has been completely reviewed.",
            reason="Fixtures explicitly require real paper review.",
        ),
        UnsafeClaim(
            text="SparseConv3D integration is already successful.",
            reason="That requires real experiment evidence from the evidence ledger.",
        ),
    ]
    for score in risk_scores:
        if score.level in {CollisionRiskLevel.HIGH, CollisionRiskLevel.UNKNOWN}:
            claims.append(
                UnsafeClaim(
                    text=f"{score.title} is safe to ignore.",
                    reason=f"{score.title} has {score.level} collision risk and needs review.",
                )
            )
    return claims
