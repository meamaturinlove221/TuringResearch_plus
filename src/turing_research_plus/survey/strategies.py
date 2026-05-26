"""Literature survey strategy routing and defaults."""

from __future__ import annotations

from turing_research_plus.survey.models import SurveyInput, SurveyPlan, SurveyStrategy


def strategy_defaults(strategy: SurveyStrategy) -> tuple[int, int, float]:
    """Return search budget, screening budget, and default full-text ratio."""

    defaults = {
        SurveyStrategy.SCOPING: (25, 15, 0.3),
        SurveyStrategy.SYSTEMATIC: (100, 50, 0.7),
        SurveyStrategy.DEEP: (60, 30, 0.85),
        SurveyStrategy.NARRATIVE: (40, 20, 0.5),
        SurveyStrategy.SNOWBALL: (80, 40, 0.6),
    }
    return defaults[strategy]


def create_survey_plan(survey_input: SurveyInput, survey_id: str = "survey-1") -> SurveyPlan:
    """Create a strategy-specific survey plan."""

    search_budget, screening_budget, default_ratio = strategy_defaults(survey_input.strategy)
    ratio = max(survey_input.full_text_ratio, default_ratio)
    return SurveyPlan(
        survey_id=survey_id,
        survey_input=survey_input.model_copy(update={"full_text_ratio": ratio}),
        search_budget=max(search_budget, survey_input.min_papers),
        screening_budget=max(screening_budget, survey_input.min_papers),
        full_text_target=max(1, int(survey_input.min_papers * ratio)),
        notes=[f"Strategy routed to {survey_input.strategy}"],
    )
