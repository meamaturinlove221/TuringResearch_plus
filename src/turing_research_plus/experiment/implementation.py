"""Experiment implementation planning."""

from __future__ import annotations

from tuling_research_plus.experiment.models import ExperimentPlan, ImplementationPlan


def build_implementation_plan(plan: ExperimentPlan) -> ImplementationPlan:
    """Build a dry-run implementation plan."""

    return ImplementationPlan(
        plan_id=plan.plan_id,
        steps=[
            *plan.implementation_steps,
            "Validate result schema.",
            "Write dry-run result artifact.",
        ],
        artifacts_to_create=[
            f"result-schema-{plan.plan_id}",
            f"experiment-result-{plan.plan_id}",
        ],
        dry_run=True,
    )

