from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.convergence.feasibility import assess_feasibility
from tuling_research_plus.convergence.models import CandidateKind, ConvergenceCandidate
from tuling_research_plus.convergence.service import ConvergenceService
from tuling_research_plus.convergence.tools import research_feasibility_assess


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def candidate(feasibility: float) -> ConvergenceCandidate:
    return ConvergenceCandidate(
        candidate_id="candidate-1",
        kind=CandidateKind.EXPERIMENT,
        title="Experiment candidate",
        mechanism="evidence gate",
        expected_gain="Lower unsupported claim rate.",
        feasibility=feasibility,
        novelty=0.7,
        risk="medium",
        required_resources=["audit table"],
        evidence_refs=[evidence()],
    )


def test_feasibility_assessment_marks_blockers() -> None:
    assessment = assess_feasibility(candidate(0.4))

    assert assessment.feasible is False
    assert assessment.blockers == ["feasibility below promotion threshold"]


def test_feasibility_tool_returns_json_payload() -> None:
    payload = research_feasibility_assess(candidate(0.8), ConvergenceService())

    assert payload["feasible"] is True
    assert payload["notes"]

