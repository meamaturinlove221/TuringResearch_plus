import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.experiment.design import design_experiment
from turing_research_plus.experiment.models import ExperimentPlan
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


def test_experiment_plan_contains_required_fields() -> None:
    plan = design_experiment(hypothesis())

    assert plan.hypothesis.hypothesis_id == "hypothesis-1"
    assert plan.variables["independent"]
    assert plan.controls
    assert plan.datasets
    assert plan.metrics
    assert plan.baselines
    assert plan.ablations
    assert plan.expected_outcomes
    assert plan.failure_modes
    assert plan.compute_budget.max_runtime_minutes > 0
    assert plan.implementation_steps
    assert plan.reproducibility_checklist
    assert plan.statistical_comparison_plan.primary_test


def test_experiment_plan_requires_controls_metrics_and_ablations() -> None:
    payload = design_experiment(hypothesis()).model_dump()
    payload["controls"] = []
    payload["metrics"] = []
    payload["ablations"] = []

    with pytest.raises(ValidationError):
        ExperimentPlan(**payload)


def test_experiment_plan_converts_to_research_artifact() -> None:
    artifact = design_experiment(hypothesis()).to_research_artifact()

    assert artifact.evidence
    assert "experiment_plan" in artifact.tags

