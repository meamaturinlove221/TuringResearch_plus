from __future__ import annotations

import pytest

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence.models import (
    CandidateKind,
    CandidateScore,
    ConvergenceCandidate,
    DecisionReport,
    FeasibilityAssessment,
)


def evidence(source_id: str = "source-1") -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-1",
        quote="Fake evidence for deterministic route comparison.",
    )


def candidate(candidate_id: str = "route-a") -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.RELEASE_FEATURE,
        title=f"Route {candidate_id}",
        mechanism="local review workflow",
        expected_gain="Improve release decision quality.",
        feasibility=0.8,
        novelty=0.7,
        risk="medium",
        required_resources=["review table"],
        evidence_refs=[evidence(candidate_id)],
    )


def score(candidate_id: str) -> CandidateScore:
    return CandidateScore(
        candidate_id=candidate_id,
        total_score=0.8,
        criteria={"feasibility": 0.8, "evidence_strength": 0.8},
        rationale="test score",
        evidence_refs=[evidence(candidate_id)],
    )


def feasibility(candidate_id: str) -> FeasibilityAssessment:
    return FeasibilityAssessment(
        candidate_id=candidate_id,
        feasible=True,
        score=0.8,
        notes=["test feasibility"],
    )


def test_decision_report_requires_final_recommendation_in_ranked_candidates() -> None:
    with pytest.raises(ValueError, match="final recommendation"):
        DecisionReport(
            report_id="bad-report",
            ranked_candidates=[score("route-a")],
            scoring_matrix={"route-a": {"feasibility": 0.8}},
            sensitivity_analysis=["test"],
            feasibility_notes=[feasibility("route-a")],
            final_recommendation="route-b",
            confidence=0.8,
            next_actions=["review"],
        )


def test_candidate_model_preserves_evidence_refs() -> None:
    item = candidate()

    assert item.candidate_id == "route-a"
    assert item.evidence_refs[0].source_id == "route-a"
