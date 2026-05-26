from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence.models import CandidateKind, ConvergenceCandidate
from turing_research_plus.convergence.portfolio import optimize_portfolio
from turing_research_plus.convergence.service import ConvergenceService
from turing_research_plus.convergence.tools import (
    research_decision_steelman,
    research_portfolio_optimize,
)


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def candidate(
    candidate_id: str,
    feasibility: float,
    novelty: float,
    resources: list[str] | None = None,
) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.RELEASE_FEATURE,
        title=f"Candidate {candidate_id}",
        mechanism="evidence gate",
        expected_gain="Promote implementation variant.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=resources or ["audit table"],
        evidence_refs=[evidence(candidate_id)],
    )


def candidates() -> list[ConvergenceCandidate]:
    return [
        candidate("candidate-promote", 0.9, 0.85),
        candidate(
            "candidate-reject",
            0.45,
            0.9,
            resources=["a", "b", "c", "d", "e"],
        ),
    ]


def test_portfolio_optimize_returns_required_decision_report_fields() -> None:
    report = optimize_portfolio(candidates())

    assert report.ranked_candidates
    assert report.scoring_matrix
    assert report.pairwise_matrix
    assert report.sensitivity_analysis
    assert report.feasibility_notes
    assert report.rejected_candidates
    assert report.steelman_for_rejected
    assert report.final_recommendation == "candidate-promote"
    assert report.confidence > 0
    assert report.next_actions
    assert report.to_research_artifact().evidence


def test_portfolio_optimize_tool_and_steelman_tool() -> None:
    service = ConvergenceService()
    report = optimize_portfolio(candidates())
    payload = research_portfolio_optimize(candidates(), service)
    steelman = research_decision_steelman(report, service)

    assert payload["final_recommendation"] == "candidate-promote"
    assert "candidate-reject" in steelman

