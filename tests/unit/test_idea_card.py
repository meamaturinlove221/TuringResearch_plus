import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.race.models import (
    IdeaCard,
    IdeaPriority,
    RecommendedAction,
    SourceHygieneGate,
    SourceHygieneStatus,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="public-src", locator="README", quote="Public reference.")


def test_idea_card_requires_passed_source_hygiene_gate() -> None:
    gate = SourceHygieneGate(
        status=SourceHygieneStatus.PASSED,
        checked_sources=[evidence()],
    )

    card = IdeaCard(
        idea_id="idea-1",
        title="MCP-first workflow",
        raw_text="MCP-first workflow should use a service protocol boundary.",
        normalized_summary="MCP-first workflow should use a service protocol boundary.",
        inferred_intent="Improve MCP-first workflow tooling.",
        source="public-src",
        value_score=0.8,
        feasibility_score=0.7,
        urgency_score=0.6,
        novelty_score=0.7,
        priority=IdeaPriority.MEDIUM,
        recommended_action=RecommendedAction.WATCH,
        evidence_refs=[evidence()],
        uncertain_terms=[],
        hypothesis="A service-protocol boundary keeps Fusion independent.",
        evidence=[evidence()],
        hygiene_gate=gate,
    )

    assert card.hygiene_gate.status == SourceHygieneStatus.PASSED
    assert card.evidence_refs[0].source_id == "public-src"
    assert card.priority == IdeaPriority.MEDIUM


def test_idea_card_allows_blocked_hygiene_gate_for_watch() -> None:
    gate = SourceHygieneGate(
        status=SourceHygieneStatus.BLOCKED,
        blocked_reason="Source is not public.",
    )

    card = IdeaCard(
        idea_id="idea-1",
        title="Blocked idea",
        hypothesis="Should not become implementation work.",
        evidence=[evidence()],
        hygiene_gate=gate,
        recommended_action=RecommendedAction.WATCH,
    )

    assert card.recommended_action == RecommendedAction.WATCH


def test_idea_card_rejects_implementation_with_blocked_hygiene_gate() -> None:
    gate = SourceHygieneGate(
        status=SourceHygieneStatus.BLOCKED,
        blocked_reason="Source is not public.",
    )

    with pytest.raises(ValidationError):
        IdeaCard(
            idea_id="idea-1",
            title="Blocked implementation",
            hypothesis="Should not become implementation work.",
            evidence=[evidence()],
            hygiene_gate=gate,
            recommended_action=RecommendedAction.IMPLEMENT,
        )
