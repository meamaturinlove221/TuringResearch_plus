from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.convergence.models import CandidateKind, ConvergenceCandidate
from turing_research_plus.convergence.scoring import score_candidate, scoring_matrix
from turing_research_plus.convergence.service import ConvergenceService
from turing_research_plus.convergence.tools import research_candidate_score


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def candidate(candidate_id: str = "candidate-1") -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id=candidate_id,
        kind=CandidateKind.IDEA,
        title="Evaluate gate thresholds",
        mechanism="evidence gate",
        expected_gain="Lower unsupported claim rate.",
        feasibility=0.8,
        novelty=0.75,
        risk="medium",
        required_resources=["audit table"],
        evidence_refs=[evidence()],
    )


def test_candidate_score_contains_explicit_matrix_criteria() -> None:
    score = score_candidate(candidate())

    assert score.candidate_id == "candidate-1"
    assert score.total_score > 0
    assert {
        "evidence_strength",
        "feasibility",
        "novelty",
        "expected_gain",
        "risk_adjustment",
    } <= set(score.criteria)
    assert score.evidence_refs


def test_scoring_matrix_is_keyed_by_candidate_id() -> None:
    scores = [score_candidate(candidate("candidate-1"))]
    matrix = scoring_matrix(scores)

    assert matrix["candidate-1"]["feasibility"] == 0.8


def test_candidate_score_tool_returns_json_payload() -> None:
    payload = research_candidate_score(candidate(), ConvergenceService())

    assert payload["candidate_id"] == "candidate-1"
    assert payload["criteria"]["evidence_strength"] > 0
