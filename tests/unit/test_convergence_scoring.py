from __future__ import annotations

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence.models import CandidateKind, ConvergenceCandidate
from turing_research_plus.convergence.scoring import score_candidate, score_candidates


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-1",
        quote="Fake evidence for deterministic scoring.",
    )


def candidate(candidate_id: str, feasibility: float, novelty: float) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.IMPLEMENTATION_VARIANT,
        title=f"Route {candidate_id}",
        mechanism="route comparison",
        expected_gain="Improve implementation quality.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=["review"],
        evidence_refs=[evidence(candidate_id)],
    )


def test_score_candidate_uses_explicit_criteria() -> None:
    scored = score_candidate(candidate("route-a", 0.9, 0.8))

    assert scored.total_score > 0.7
    assert {
        "evidence_strength",
        "feasibility",
        "novelty",
        "expected_gain",
        "risk_adjustment",
    } <= set(scored.criteria)


def test_score_candidates_ranks_highest_score_first() -> None:
    ranked = score_candidates(
        [
            candidate("route-low", 0.55, 0.5),
            candidate("route-high", 0.9, 0.9),
        ]
    )

    assert ranked[0].candidate_id == "route-high"
