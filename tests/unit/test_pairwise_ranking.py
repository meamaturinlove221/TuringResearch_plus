from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence.models import CandidateKind, ConvergenceCandidate
from turing_research_plus.convergence.pairwise import pairwise_rank
from turing_research_plus.convergence.scoring import score_candidates
from turing_research_plus.convergence.service import ConvergenceService
from turing_research_plus.convergence.tools import research_candidate_pairwise_rank


def evidence(source_id: str) -> EvidenceRef:
    return EvidenceRef(
        source_id=source_id,
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def candidate(candidate_id: str, feasibility: float, novelty: float) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.IDEA,
        title=f"Candidate {candidate_id}",
        mechanism="evidence gate",
        expected_gain="Lower unsupported claim rate.",
        feasibility=feasibility,
        novelty=novelty,
        risk="medium",
        required_resources=["audit table"],
        evidence_refs=[evidence(candidate_id)],
    )


def candidates() -> list[ConvergenceCandidate]:
    return [
        candidate("candidate-high", 0.9, 0.85),
        candidate("candidate-low", 0.55, 0.5),
    ]


def test_pairwise_ranking_selects_higher_score() -> None:
    preferences = pairwise_rank(score_candidates(candidates()))

    assert preferences[0].winner_id == "candidate-high"
    assert preferences[0].margin > 0


def test_pairwise_tool_returns_json_payload() -> None:
    payload = research_candidate_pairwise_rank(candidates(), ConvergenceService())

    assert payload[0]["winner_id"] == "candidate-high"
    assert payload[0]["left_id"]
    assert payload[0]["right_id"]

