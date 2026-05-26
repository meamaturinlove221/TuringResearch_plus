"""Experiment design generation."""

from __future__ import annotations

from tuling_research_plus.experiment.models import (
    ComputeBudget,
    ExperimentPlan,
    StatisticalComparisonPlan,
)
from tuling_research_plus.hypothesis.models import Hypothesis


def design_experiment(hypothesis: Hypothesis, plan_id: str = "experiment-plan-1") -> ExperimentPlan:
    """Design a deterministic experiment plan from a validated hypothesis."""

    return ExperimentPlan(
        plan_id=plan_id,
        hypothesis=hypothesis,
        variables={
            "independent": hypothesis.independent_variables,
            "dependent": hypothesis.dependent_variables,
            "control": hypothesis.control_variables,
        },
        controls=hypothesis.control_variables,
        datasets=hypothesis.required_experiment.required_data,
        metrics=[
            hypothesis.required_experiment.measurement,
            *hypothesis.dependent_variables,
        ],
        baselines=["baseline workflow output", "ungated workflow output"],
        ablations=[
            "remove evidence gate",
            "remove control variables",
        ],
        expected_outcomes=hypothesis.success_criteria,
        failure_modes=[
            hypothesis.failure_interpretation,
            hypothesis.falsifiability_criteria.falsifying_observation,
        ],
        compute_budget=ComputeBudget(
            max_runtime_minutes=30,
            max_cost_units=0.0,
            resource_class="local-dry-run",
        ),
        implementation_steps=[
            "Prepare baseline artifact set.",
            "Run dry-run treatment with proposed variables.",
            "Collect metrics according to result schema.",
        ],
        reproducibility_checklist=[
            "Record input artifact ids.",
            "Record deterministic seed or fake-service fixture.",
            "Store result schema and metric definitions.",
        ],
        statistical_comparison_plan=StatisticalComparisonPlan(
            primary_test="paired deterministic comparison",
            confidence_level=0.95,
            correction="none",
            effect_size_metric=hypothesis.required_experiment.measurement,
        ),
        evidence_refs=hypothesis.evidence_refs,
    )

