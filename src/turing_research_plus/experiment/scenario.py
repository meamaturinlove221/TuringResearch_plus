"""Experiment scenario planning."""

from __future__ import annotations

from tuling_research_plus.experiment.models import ExperimentPlan, ScenarioPlan


def plan_scenarios(plan: ExperimentPlan) -> ScenarioPlan:
    """Create best, expected, and worst-case scenarios."""

    primary_metric = plan.metrics[0]
    return ScenarioPlan(
        plan_id=plan.plan_id,
        best_case=f"{primary_metric} improves and all controls remain stable.",
        expected_case=f"{primary_metric} changes in the expected direction with minor noise.",
        worst_case=f"{primary_metric} fails to improve or reverses.",
        fallback_actions=[
            "Inspect failure modes.",
            "Run ablation comparison.",
            "Revisit hypothesis boundary conditions.",
        ],
    )

