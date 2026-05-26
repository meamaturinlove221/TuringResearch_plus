from __future__ import annotations

from turing_research_plus.experiment_execution.artifact_requirements import (
    build_artifact_requirements,
)
from turing_research_plus.experiment_execution.models import ExecutionPlanStatus
from turing_research_plus.experiment_execution.plan_builder import (
    build_experiment_execution_plan,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec


def route_spec() -> ExperimentRouteSpec:
    return ExperimentRouteSpec(
        route_id="route-247",
        goal="Plan a safe fake experiment route.",
        context="demo only; not executed",
        forbidden_actions=["claim experiment completion"],
        hard_gates=["no_promotion"],
        artifact_requirements=["review bundle", "run metadata"],
        stages=[
            {
                "id": "prepare",
                "name": "Prepare",
                "purpose": "Prepare review bundle.",
                "outputs": ["artifact index"],
                "hard_gates": ["artifact_required"],
            }
        ],
    )


def test_build_artifact_requirements_from_route() -> None:
    requirements = build_artifact_requirements(route_spec())

    descriptions = {item.description for item in requirements}
    assert "review bundle" in descriptions
    assert "run metadata" in descriptions
    assert "artifact index" in descriptions
    assert all(item.requires_human_review for item in requirements)


def test_build_experiment_execution_plan_is_safe_and_ready_for_human_run() -> None:
    plan = build_experiment_execution_plan(route_spec())

    assert plan.status == ExecutionPlanStatus.READY_FOR_HUMAN_RUN
    assert plan.blockers == []
    assert plan.automatically_executes is False
    assert plan.remote_execution is False
    assert plan.modal_call is False
    assert plan.gpu_call is False
    assert plan.writes_observed_result is False
    assert plan.ingest_contract.proposed_evidence_only is True
    assert plan.ingest_contract.writes_observed_result is False
    assert "artifact_required" in plan.hard_gates
    assert "no_promotion" in plan.hard_gates


def test_build_experiment_execution_plan_blocks_missing_artifacts_and_gates() -> None:
    route = ExperimentRouteSpec(
        route_id="blocked-route",
        goal="Plan blocked route.",
        context="demo only; not executed",
        forbidden_actions=["claim experiment completion"],
        stages=[
            {
                "id": "prepare",
                "name": "Prepare",
                "purpose": "Prepare.",
            }
        ],
    )

    plan = build_experiment_execution_plan(route)

    assert plan.status == ExecutionPlanStatus.BLOCKED
    assert "missing-artifact-requirements" in plan.blockers
    assert "missing-hard-gates" in plan.blockers
