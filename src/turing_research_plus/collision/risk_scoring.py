"""Risk scoring for paper collision reports."""

from __future__ import annotations

from turing_research_plus.collision.models import (
    CollisionRiskLevel,
    OverlapDimension,
    OverlapMatrix,
    RiskScore,
)

HIGH_WEIGHT_DIMENSIONS = {
    OverlapDimension.TASK,
    OverlapDimension.REPRESENTATION,
    OverlapDimension.SMPL_SMPLX_ENCODING,
    OverlapDimension.VGGT_TOKEN_INTEGRATION,
    OverlapDimension.CLAIMED_CONTRIBUTION,
}


def score_collision_risk(
    compared_papers: list[dict[str, object]],
    overlap_matrix: OverlapMatrix,
) -> list[RiskScore]:
    """Aggregate overlap matrix rows into conservative risk levels."""

    scores: list[RiskScore] = []
    for paper in compared_papers:
        paper_id = str(paper.get("paper_id") or paper.get("paperId") or paper.get("title"))
        title = str(paper.get("title") or paper_id)
        rows = overlap_matrix.for_paper(paper_id)
        if not rows:
            scores.append(_unknown(paper_id, title, "No overlap rows were available."))
            continue
        weighted = []
        for row in rows:
            weight = 1.5 if row.dimension in HIGH_WEIGHT_DIMENSIONS else 1.0
            weighted.append(row.score * weight)
        total_weight = sum(1.5 if r.dimension in HIGH_WEIGHT_DIMENSIONS else 1.0 for r in rows)
        score = round(sum(weighted) / total_weight, 3)
        level = _level_for(score, paper)
        scores.append(
            RiskScore(
                paper_id=paper_id,
                title=title,
                level=level,
                score=score,
                rationale=_rationale(title, score, level),
                requires_human_review=True,
            )
        )
    return scores


def _level_for(score: float, paper: dict[str, object]) -> CollisionRiskLevel:
    text = " ".join(str(value) for value in paper.values()).lower()
    if "requires-real-paper-review" in text:
        return CollisionRiskLevel.UNKNOWN if score < 0.55 else CollisionRiskLevel.MEDIUM
    if "hart" in text and score >= 0.35:
        return CollisionRiskLevel.HIGH
    if score >= 0.6:
        return CollisionRiskLevel.HIGH
    if score >= 0.3:
        return CollisionRiskLevel.MEDIUM
    return CollisionRiskLevel.LOW


def _unknown(paper_id: str, title: str, rationale: str) -> RiskScore:
    return RiskScore(
        paper_id=paper_id,
        title=title,
        level=CollisionRiskLevel.UNKNOWN,
        score=0,
        rationale=rationale,
        requires_human_review=True,
    )


def _rationale(title: str, score: float, level: CollisionRiskLevel) -> str:
    return (
        f"{title} has {level} collision risk score {score}; this is a fixture-based "
        "screen and requires human review."
    )
