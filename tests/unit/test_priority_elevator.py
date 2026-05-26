from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.race.models import IdeaCard, SourceHygieneGate, SourceHygieneStatus
from turing_research_plus.race.priority_elevator import (
    RacePriority,
    priority_score,
    race_priority_score,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="public-src",
        locator="README",
        quote="Public source describes a useful feature.",
    )


def gate(status: SourceHygieneStatus = SourceHygieneStatus.PASSED) -> SourceHygieneGate:
    if status == SourceHygieneStatus.PASSED:
        return SourceHygieneGate(status=status, checked_sources=[evidence()])
    return SourceHygieneGate(
        status=status,
        checked_sources=[evidence()],
        blocked_reason="Source hygiene blocked.",
    )


def idea(
    value: float = 0.9,
    urgency: float = 0.9,
    feasibility: float = 0.85,
    novelty: float = 0.8,
    hygiene_status: SourceHygieneStatus = SourceHygieneStatus.PASSED,
) -> IdeaCard:
    return IdeaCard(
        idea_id="idea-1",
        title="Priority idea",
        raw_text="Urgent public idea.",
        normalized_summary="Urgent public idea.",
        inferred_intent="Improve Race Mode prioritization.",
        source="public-src",
        value_score=value,
        feasibility_score=feasibility,
        urgency_score=urgency,
        novelty_score=novelty,
        evidence_refs=[evidence()],
        hygiene_gate=gate(hygiene_status),
    )


def test_deterministic_scoring() -> None:
    first = priority_score(idea(), strategic_fit=0.8)
    second = priority_score(idea(), strategic_fit=0.8)

    assert first == second
    assert first.priority_score == 0.865


def test_p0_threshold_works() -> None:
    result = priority_score(idea(), strategic_fit=0.8)

    assert result.priority == RacePriority.P0
    assert result.recommendation == "prototype immediately"


def test_blocked_source_cannot_become_p0() -> None:
    result = priority_score(
        idea(hygiene_status=SourceHygieneStatus.BLOCKED),
        strategic_fit=1.0,
    )

    assert result.priority == RacePriority.P2
    assert result.blocked_by_source_hygiene is True
    assert result.should_create_feature_capsule is False


def test_feature_capsule_recommendation_generated_for_p1() -> None:
    result = priority_score(
        idea(value=0.78, urgency=0.75, feasibility=0.74, novelty=0.7),
        strategic_fit=0.7,
    )

    assert result.priority == RacePriority.P1
    assert result.should_create_feature_capsule is True
    assert result.recommendation == "create feature capsule this sprint"


def test_race_priority_score_tool_returns_json_payload() -> None:
    payload = race_priority_score(idea(), strategic_fit=0.8)

    assert payload["priority"] == "P0"
    assert payload["priority_score"] == 0.865
