from turing_research_plus.survey.depth_gate import evaluate_depth_gates, full_text_ratio
from turing_research_plus.survey.models import (
    PaperScreeningDecision,
    PaperScreeningRow,
    PaperScreeningTable,
    SurveyInput,
    SurveyStrategy,
)


def screening(full_text_count: int, included_count: int) -> PaperScreeningTable:
    rows = [
        PaperScreeningRow(
            paper_id=f"p{index}",
            title=f"Paper {index}",
            decision=PaperScreeningDecision.INCLUDE,
            reason="fixture",
            full_text_available=index < full_text_count,
        )
        for index in range(included_count)
    ]
    return PaperScreeningTable(rows=rows)


def test_overview_cannot_make_strong_conclusions() -> None:
    blockers = evaluate_depth_gates(
        SurveyInput(
            topic="overview",
            strategy=SurveyStrategy.SCOPING,
            min_papers=1,
            research_goal="Overview.",
        ),
        screening(full_text_count=1, included_count=1),
        conclusion_strength="overview",
    )

    assert "overview cannot produce strong conclusions" in blockers


def test_deep_survey_must_satisfy_full_text_ratio() -> None:
    blockers = evaluate_depth_gates(
        SurveyInput(
            topic="deep",
            strategy=SurveyStrategy.DEEP,
            min_papers=4,
            full_text_ratio=0.75,
            research_goal="Deep synthesis.",
        ),
        screening(full_text_count=2, included_count=4),
    )

    assert full_text_ratio(screening(full_text_count=2, included_count=4)) == 0.5
    assert "deep survey full_text_ratio not satisfied" in blockers
