from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.experiment.design import design_experiment
from tuling_research_plus.experiment.service import ExperimentExecutionService
from tuling_research_plus.experiment.tools import research_experiment_design
from tuling_research_plus.hypothesis.falsifiability import build_hypothesis
from tuling_research_plus.hypothesis.models import GapPriority, Hypothesis


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


def test_experiment_design_maps_hypothesis_variables() -> None:
    plan = design_experiment(hypothesis())

    assert plan.variables["independent"] == hypothesis().independent_variables
    assert plan.variables["dependent"] == hypothesis().dependent_variables
    assert plan.variables["control"] == hypothesis().control_variables
    assert plan.evidence_refs


def test_experiment_design_tool_returns_json_payload() -> None:
    payload = research_experiment_design(hypothesis(), ExperimentExecutionService())

    assert payload["plan_id"] == "experiment-plan-1"
    assert payload["controls"]
    assert payload["metrics"]
    assert payload["ablations"]

