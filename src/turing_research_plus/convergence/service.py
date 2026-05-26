"""Convergence workflow service."""

from __future__ import annotations

from turing_research_plus.convergence.feasibility import assess_feasibility
from turing_research_plus.convergence.models import (
    CandidateScore,
    ConvergenceCandidate,
    DecisionReport,
    FeasibilityAssessment,
    PairwisePreference,
    PromotionDecisionResult,
)
from turing_research_plus.convergence.pairwise import pairwise_rank
from turing_research_plus.convergence.portfolio import decide_promotion, optimize_portfolio
from turing_research_plus.convergence.scoring import score_candidate, score_candidates


class ConvergenceService:
    """Rank alternatives and produce convergence decisions."""

    def candidate_score(self, candidate: ConvergenceCandidate) -> CandidateScore:
        """Score one candidate."""

        return score_candidate(candidate)

    def candidate_pairwise_rank(
        self,
        candidates: list[ConvergenceCandidate],
    ) -> list[PairwisePreference]:
        """Rank candidates pairwise."""

        return pairwise_rank(score_candidates(candidates))

    def feasibility_assess(
        self,
        candidate: ConvergenceCandidate,
    ) -> FeasibilityAssessment:
        """Assess candidate feasibility."""

        return assess_feasibility(candidate)

    def portfolio_optimize(
        self,
        candidates: list[ConvergenceCandidate],
        include_pairwise: bool = True,
    ) -> DecisionReport:
        """Optimize candidate portfolio."""

        return optimize_portfolio(candidates, include_pairwise=include_pairwise)

    def decision_steelman(
        self,
        report: DecisionReport,
    ) -> dict[str, str]:
        """Return steelman notes for rejected candidates."""

        return report.steelman_for_rejected

    def promotion_decide(
        self,
        score: CandidateScore,
        feasible: bool = True,
    ) -> PromotionDecisionResult:
        """Promote, reject, or hold one candidate."""

        return decide_promotion(score, feasible=feasible)
