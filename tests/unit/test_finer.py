from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.hypothesis.falsifiability import build_hypothesis
from turing_research_plus.hypothesis.finer import assess_finer, formulate_research_question
from turing_research_plus.hypothesis.models import GapPriority, Hypothesis
from turing_research_plus.hypothesis.service import HypothesisFormationService
from turing_research_plus.hypothesis.tools import research_research_question_formulate


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def hypothesis() -> Hypothesis:
    return build_hypothesis(
        GapPriority(
            gap_id="gap-1",
            description="Few studies validate workflow gates.",
            score=0.9,
            rationale="High confidence and enough evidence.",
            evidence=[evidence()],
        )
    ).model_copy(update={"score": 0.88})


def test_finer_assessment_scores_all_dimensions() -> None:
    assessment = assess_finer(hypothesis())

    assert assessment.feasible > 0
    assert assessment.interesting > 0
    assert assessment.novel > 0
    assert assessment.ethical > 0
    assert assessment.relevant > 0
    assert 0 <= assessment.overall <= 1


def test_formulate_research_question_is_precise() -> None:
    question = formulate_research_question(hypothesis())

    assert question.question.startswith("To what extent")
    assert question.hypothesis_id == "hypothesis-1"
    assert question.evidence_refs


def test_research_question_tool_returns_json_payload() -> None:
    payload = research_research_question_formulate(hypothesis(), HypothesisFormationService())

    assert payload["question_id"] == "rq-hypothesis-1"
    assert payload["finer_score"] > 0
