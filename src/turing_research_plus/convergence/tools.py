"""Thin research.convergence_* tool wrappers."""

from __future__ import annotations

from typing import Any

from turing_research_plus.convergence.models import (
    CandidateScore,
    ConvergenceCandidate,
    DecisionReport,
)
from turing_research_plus.convergence.service import ConvergenceService


def research_candidate_score(
    candidate: ConvergenceCandidate,
    service: ConvergenceService,
) -> dict[str, Any]:
    return service.candidate_score(candidate).model_dump(mode="json")


def research_candidate_pairwise_rank(
    candidates: list[ConvergenceCandidate],
    service: ConvergenceService,
) -> list[dict[str, Any]]:
    return [
        preference.model_dump(mode="json")
        for preference in service.candidate_pairwise_rank(candidates)
    ]


def research_feasibility_assess(
    candidate: ConvergenceCandidate,
    service: ConvergenceService,
) -> dict[str, Any]:
    return service.feasibility_assess(candidate).model_dump(mode="json")


def research_portfolio_optimize(
    candidates: list[ConvergenceCandidate],
    service: ConvergenceService,
    include_pairwise: bool = True,
) -> dict[str, Any]:
    return service.portfolio_optimize(
        candidates,
        include_pairwise=include_pairwise,
    ).model_dump(mode="json")


def research_decision_steelman(
    report: DecisionReport,
    service: ConvergenceService,
) -> dict[str, str]:
    return service.decision_steelman(report)


def research_promotion_decide(
    score: CandidateScore,
    service: ConvergenceService,
    feasible: bool = True,
) -> dict[str, Any]:
    return service.promotion_decide(score, feasible=feasible).model_dump(mode="json")

