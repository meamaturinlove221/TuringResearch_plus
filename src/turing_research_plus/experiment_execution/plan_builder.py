"""Build safe experiment execution plans from route specs."""

from __future__ import annotations

from turing_research_plus.experiment_execution.artifact_requirements import (
    build_artifact_requirements,
)
from turing_research_plus.experiment_execution.models import (
    ArtifactRequirement,
    ExecutionPlanStatus,
    ExperimentExecutionPlan,
    RunIngestContract,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec
from turing_research_plus.run_ingest.models import RunSourceType


def build_experiment_execution_plan(route: ExperimentRouteSpec) -> ExperimentExecutionPlan:
    """Create a review-only execution plan without running anything."""

    artifact_requirements = build_artifact_requirements(route)
    hard_gates = sorted(
        {
            gate
            for gate in [
                *route.hard_gates,
                *(gate for stage in route.stages for gate in stage.hard_gates),
            ]
        }
    )
    forbidden_actions = sorted(set(route.forbidden_actions))
    blockers = _collect_blockers(route, artifact_requirements, hard_gates)
    status = (
        ExecutionPlanStatus.BLOCKED
        if blockers
        else ExecutionPlanStatus.READY_FOR_HUMAN_RUN
    )
    ingest_contract = RunIngestContract(
        route_id=route.route_id,
        accepted_source_types=[item.value for item in RunSourceType],
        required_metadata=[
            "run_id",
            "route_id",
            "source_type",
            "run_status",
            "duration",
            "hard_gate_results",
            "missing_artifacts",
        ],
        required_artifacts=[item.description for item in artifact_requirements],
    )
    return ExperimentExecutionPlan(
        plan_id=f"{route.route_id}-safe-execution-plan",
        route_id=route.route_id,
        goal=route.goal,
        status=status,
        runbook_steps=_build_runbook_steps(route, artifact_requirements, hard_gates),
        artifact_requirements=artifact_requirements,
        hard_gates=hard_gates,
        forbidden_actions=forbidden_actions,
        ingest_contract=ingest_contract,
        blockers=blockers,
    )


def _collect_blockers(
    route: ExperimentRouteSpec,
    artifact_requirements: list[ArtifactRequirement],
    hard_gates: list[str],
) -> list[str]:
    blockers: list[str] = []
    forbidden_text = " ".join(route.forbidden_actions).lower()
    if "claim experiment completion" not in forbidden_text:
        blockers.append("missing-forbidden-completion-claim-boundary")
    if not artifact_requirements:
        blockers.append("missing-artifact-requirements")
    if not hard_gates:
        blockers.append("missing-hard-gates")
    return blockers


def _build_runbook_steps(
    route: ExperimentRouteSpec,
    artifact_requirements: list[ArtifactRequirement],
    hard_gates: list[str],
) -> list[str]:
    return [
        f"Review route `{route.route_id}` and confirm human owner.",
        "Prepare artifacts listed in artifact requirements.",
        f"Validate hard gates: {', '.join(hard_gates) or 'none'}.",
        "Human operator runs experiment outside TuringResearch if approved.",
        "Ingest exported run bundle with run ingest contract.",
        "Review proposed evidence updates; do not write observed result automatically.",
        f"Expected artifact count: {len(artifact_requirements)}.",
    ]
