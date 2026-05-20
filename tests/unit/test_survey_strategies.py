from tuling_research_plus.survey.models import SurveyInput, SurveyStrategy
from tuling_research_plus.survey.strategies import create_survey_plan, strategy_defaults


def test_strategy_routing_and_budget_defaults() -> None:
    survey_input = SurveyInput(
        topic="semantic graphs",
        strategy=SurveyStrategy.DEEP,
        min_papers=10,
        full_text_ratio=0.2,
        research_goal="Understand evidence.",
    )

    plan = create_survey_plan(survey_input)

    assert strategy_defaults(SurveyStrategy.DEEP) == (60, 30, 0.85)
    assert plan.search_budget == 60
    assert plan.screening_budget == 30
    assert plan.survey_input.full_text_ratio == 0.85
    assert plan.full_text_target == 8


def test_snowball_strategy_defaults() -> None:
    plan = create_survey_plan(
        SurveyInput(
            topic="citation expansion",
            strategy=SurveyStrategy.SNOWBALL,
            seed_papers=["seed"],
            research_goal="Trace lineage.",
        )
    )

    assert plan.search_budget == 80
    assert plan.survey_input.seed_papers == ["seed"]
