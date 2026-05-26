"""Markdown runbook rendering for safe experiment execution plans."""

from __future__ import annotations

from turing_research_plus.experiment_execution.models import ExperimentExecutionPlan


def render_experiment_execution_runbook(plan: ExperimentExecutionPlan) -> str:
    """Render a safe experiment execution plan as Markdown."""

    blocker_lines = [f"- `{item}`" for item in plan.blockers] or ["- none"]
    artifact_lines = [
        f"- `{item.artifact_id}`: {item.description}" for item in plan.artifact_requirements
    ] or ["- none"]
    gate_lines = [f"- `{item}`" for item in plan.hard_gates] or ["- none"]
    step_lines = [f"{index}. {step}" for index, step in enumerate(plan.runbook_steps, start=1)]
    lines = [
        f"# Safe Experiment Execution Runbook: {plan.route_id}",
        "",
        f"- Plan id: `{plan.plan_id}`",
        f"- Status: `{plan.status.value}`",
        f"- Requires human review: `{str(plan.requires_human_review).lower()}`",
        "- Automatically executes: `false`",
        "- Remote execution: `false`",
        "- Modal call: `false`",
        "- GPU call: `false`",
        "- Writes observed result: `false`",
        "",
        "## Blockers",
        "",
        *blocker_lines,
        "",
        "## Runbook Steps",
        "",
        *step_lines,
        "",
        "## Artifact Requirements",
        "",
        *artifact_lines,
        "",
        "## Hard Gates",
        "",
        *gate_lines,
        "",
        "## Run Ingest Contract",
        "",
        f"- Proposed evidence only: `{str(plan.ingest_contract.proposed_evidence_only).lower()}`",
        f"- Writes observed result: `{str(plan.ingest_contract.writes_observed_result).lower()}`",
    ]
    return "\n".join(lines) + "\n"
