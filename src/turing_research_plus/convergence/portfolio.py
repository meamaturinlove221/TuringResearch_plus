"""Portfolio optimization and promotion decisions."""

from __future__ import annotations

from turing_research_plus.convergence.feasibility import assess_feasibilities
from turing_research_plus.convergence.models import (
    CandidateScore,
    ConvergenceCandidate,
    DecisionReport,
    PromotionDecision,
    PromotionDecisionResult,
)
from turing_research_plus.convergence.pairwise import pairwise_rank
from turing_research_plus.convergence.scoring import score_candidates, scoring_matrix


def optimize_portfolio(
    candidates: list[ConvergenceCandidate],
    report_id: str = "decision-report-1",
    include_pairwise: bool = True,
) -> DecisionReport:
    """Build a deterministic decision report."""

    scores = score_candidates(candidates)
    feasibilities = assess_feasibilities(candidates)
    feasible_ids = {
        feasibility.candidate_id
        for feasibility in feasibilities
        if feasibility.feasible
    }
    ranked = [score for score in scores if score.candidate_id in feasible_ids]
    rejected = [score for score in scores if score.candidate_id not in feasible_ids]
    if not ranked:
        ranked = scores[:1]
        rejected = scores[1:]
    final = ranked[0]
    return DecisionReport(
        report_id=report_id,
        ranked_candidates=ranked,
        scoring_matrix=scoring_matrix(scores),
        pairwise_matrix=pairwise_rank(scores) if include_pairwise else None,
        sensitivity_analysis=[
            "Ranking is most sensitive to feasibility and evidence strength.",
            "High resource footprint can move a candidate from promote to hold.",
        ],
        feasibility_notes=feasibilities,
        rejected_candidates=rejected,
        steelman_for_rejected=steelman_for_rejected(rejected),
        final_recommendation=final.candidate_id,
        confidence=_confidence(final),
        next_actions=[
            f"Prepare dry-run validation for {final.candidate_id}.",
            "Record decision in StateLedger before promotion.",
        ],
    )


def decide_promotion(score: CandidateScore, feasible: bool = True) -> PromotionDecisionResult:
    """Promote, reject, or hold one candidate."""

    if not feasible:
        return PromotionDecisionResult(
            candidate_id=score.candidate_id,
            decision=PromotionDecision.REJECT,
            reason="Candidate is not feasible in the current phase.",
            confidence=0.75,
        )
    if score.total_score >= 0.78:
        return PromotionDecisionResult(
            candidate_id=score.candidate_id,
            decision=PromotionDecision.PROMOTE,
            reason="Candidate passes score and feasibility thresholds.",
            confidence=score.total_score,
        )
    return PromotionDecisionResult(
        candidate_id=score.candidate_id,
        decision=PromotionDecision.HOLD,
        reason="Candidate is promising but below promotion threshold.",
        confidence=score.total_score,
    )


def steelman_for_rejected(scores: list[CandidateScore]) -> dict[str, str]:
    """Generate deterministic steelman notes for rejected candidates."""

    return {
        score.candidate_id: (
            "Strongest case: keep as a backup if feasibility improves or evidence "
            "strength increases."
        )
        for score in scores
    }


def _confidence(score: CandidateScore) -> float:
    evidence = score.criteria["evidence_strength"]
    feasibility = score.criteria["feasibility"]
    return round((score.total_score + evidence + feasibility) / 3, 3)
