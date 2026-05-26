"""Feasibility assessment for convergence candidates."""

from __future__ import annotations

from turing_research_plus.convergence.models import ConvergenceCandidate, FeasibilityAssessment


def assess_feasibility(candidate: ConvergenceCandidate) -> FeasibilityAssessment:
    """Assess candidate feasibility with local deterministic rules."""

    blockers: list[str] = []
    notes = [
        f"Requires {len(candidate.required_resources)} resource item(s).",
        f"Risk profile is {candidate.risk}.",
    ]
    if candidate.feasibility < 0.55:
        blockers.append("feasibility below promotion threshold")
    if len(candidate.required_resources) > 4:
        blockers.append("resource footprint too large for current phase")
    feasible = not blockers
    return FeasibilityAssessment(
        candidate_id=candidate.candidate_id,
        feasible=feasible,
        score=candidate.feasibility,
        notes=notes,
        blockers=blockers,
    )


def assess_feasibilities(candidates: list[ConvergenceCandidate]) -> list[FeasibilityAssessment]:
    """Assess all candidate feasibilities."""

    return [assess_feasibility(candidate) for candidate in candidates]
