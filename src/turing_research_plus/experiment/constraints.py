"""Experiment constraint analysis."""

from __future__ import annotations

from turing_research_plus.experiment.models import ConstraintAnalysis, ExperimentPlan


def analyze_constraints(plan: ExperimentPlan) -> ConstraintAnalysis:
    """Analyze deterministic feasibility constraints."""

    constraints = [
        f"compute budget: {plan.compute_budget.max_runtime_minutes} minutes",
        f"resource class: {plan.compute_budget.resource_class}",
    ]
    blockers: list[str] = []
    if not plan.controls:
        blockers.append("controls required")
    if not plan.metrics:
        blockers.append("metrics required")
    if not plan.ablations:
        blockers.append("ablations required")
    if plan.compute_budget.max_runtime_minutes < 5:
        blockers.append("compute budget too small")
    return ConstraintAnalysis(
        plan_id=plan.plan_id,
        constraints=constraints,
        blockers=blockers,
        mitigation_options=[
            "increase compute budget",
            "add missing controls, metrics, or ablations",
        ],
        feasible=not blockers,
    )
