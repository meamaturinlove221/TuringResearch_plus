import pytest
from pydantic import ValidationError

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.survey.models import (
    GapItem,
    SurveyInput,
    SurveyStrategy,
)


def test_survey_input_validates_year_range() -> None:
    with pytest.raises(ValidationError):
        SurveyInput(
            topic="agents",
            strategy=SurveyStrategy.SCOPING,
            year_range=(2025, 2020),
            research_goal="Map literature.",
        )


def test_gap_requires_evidence() -> None:
    with pytest.raises(ValidationError):
        GapItem(gap_id="gap-1", description="No evidence.", evidence=[])


def test_survey_input_contains_required_fields() -> None:
    survey_input = SurveyInput(
        topic="agent research",
        strategy=SurveyStrategy.SYSTEMATIC,
        year_range=(2020, 2026),
        min_papers=10,
        full_text_ratio=0.7,
        seed_papers=["p1"],
        research_goal="Compare methods.",
    )

    assert survey_input.topic == "agent research"
    assert survey_input.seed_papers == ["p1"]
    assert EvidenceRef(source_id="p1", locator="abstract", quote="x").source_id == "p1"
