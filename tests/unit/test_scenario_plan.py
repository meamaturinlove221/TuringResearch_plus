from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.experiment.design import design_experiment
from turing_research_plus.experiment.scenario import plan_scenarios
from turing_research_plus.experiment.service import ExperimentExecutionService
from turing_research_plus.experiment.tools import research_scenario_plan
from turing_research_plus.hypothesis.falsifiability import build_hypothesis
from turing_research_plus.hypothesis.models import GapPriority, Hypothesis


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


def test_scenario_plan_contains_cases_and_fallbacks() -> None:
    scenario = plan_scenarios(design_experiment(hypothesis()))

    assert scenario.best_case
    assert scenario.expected_case
    assert scenario.worst_case
    assert scenario.fallback_actions


def test_scenario_plan_tool_returns_json_payload() -> None:
    payload = research_scenario_plan(
        design_experiment(hypothesis()),
        ExperimentExecutionService(),
    )

    assert payload["best_case"]
    assert payload["fallback_actions"]
