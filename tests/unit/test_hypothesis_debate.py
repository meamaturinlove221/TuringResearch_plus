from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.hypothesis.falsifiability import build_hypothesis
from turing_research_plus.hypothesis.models import (
    FalsifiabilityCriteria,
    GapPriority,
    Hypothesis,
)
from turing_research_plus.stress.hypothesis_debate import debate_hypothesis
from turing_research_plus.stress.models import PassFail, Severity
from turing_research_plus.stress.service import StressTestService
from turing_research_plus.stress.tools import research_hypothesis_debate


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
    )


def test_unfalsifiable_hypothesis_is_marked() -> None:
    weak = hypothesis().model_copy(
        update={
            "falsifiability_criteria": FalsifiabilityCriteria(
                observable_prediction="prediction",
                falsifying_observation=" ",
                measurement_window="window",
                minimum_test="test",
            )
        }
    )

    report = debate_hypothesis(weak)

    assert report.pass_fail == PassFail.FAIL
    assert report.severity == Severity.HIGH
    assert report.weaknesses[0].weakness_id == "hypothesis-unfalsifiable"


def test_falsifiable_hypothesis_keeps_low_counterargument_risk() -> None:
    report = debate_hypothesis(hypothesis())

    assert report.pass_fail == PassFail.PASS
    assert report.severity == Severity.LOW
    assert report.counterarguments


def test_hypothesis_debate_tool_returns_json_payload() -> None:
    payload = research_hypothesis_debate(hypothesis(), StressTestService())

    assert payload["artifact_id"] == "hypothesis-1"
    assert payload["weaknesses"]
