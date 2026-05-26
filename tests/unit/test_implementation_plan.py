from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.experiment.design import design_experiment
from turing_research_plus.experiment.implementation import build_implementation_plan
from turing_research_plus.experiment.service import ExperimentExecutionService
from turing_research_plus.experiment.tools import research_implementation_plan
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


def test_implementation_plan_is_dry_run_and_lists_artifacts() -> None:
    plan = build_implementation_plan(design_experiment(hypothesis()))

    assert plan.dry_run is True
    assert plan.steps
    assert "result-schema-experiment-plan-1" in plan.artifacts_to_create


def test_implementation_plan_tool_returns_json_payload() -> None:
    payload = research_implementation_plan(
        design_experiment(hypothesis()),
        ExperimentExecutionService(),
    )

    assert payload["dry_run"] is True
    assert payload["artifacts_to_create"]

