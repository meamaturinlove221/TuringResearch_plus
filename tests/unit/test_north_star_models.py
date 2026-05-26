import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.north_star.models import (
    DirectionCandidate,
    DirectionCandidates,
    NorthStarStatement,
    ResearchBrief,
    StartMode,
)


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="source-1", locator="note", quote="Evidence.")


def test_research_brief_schema_validation() -> None:
    brief = ResearchBrief(
        title="Research Brief",
        problem="Problem",
        research_goal="Goal",
        scope="Scope",
        evidence=[evidence()],
    )

    assert brief.title == "Research Brief"
    assert brief.evidence[0].source_id == "source-1"


def test_research_brief_requires_evidence() -> None:
    with pytest.raises(ValidationError):
        ResearchBrief(
            title="Research Brief",
            problem="Problem",
            research_goal="Goal",
            scope="Scope",
            evidence=[],
        )


def test_direction_candidates_rank_by_score() -> None:
    candidates = DirectionCandidates(
        candidates=[
            DirectionCandidate(
                direction_id="low",
                statement="Low",
                score=0.1,
                evidence=[evidence()],
            ),
            DirectionCandidate(
                direction_id="high",
                statement="High",
                score=0.9,
                evidence=[evidence()],
            ),
        ]
    )

    assert candidates.candidates[0].direction_id == "high"


def test_north_star_statement_requires_evidence() -> None:
    with pytest.raises(ValidationError):
        NorthStarStatement(
            statement="Study workflows.",
            mode=StartMode.WARM,
            rationale="Because.",
            evidence=[],
        )
