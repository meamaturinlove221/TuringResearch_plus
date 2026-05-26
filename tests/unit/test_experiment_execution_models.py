from __future__ import annotations

import pytest

from turing_research_plus.experiment_execution.models import (
    ExecutionPlanStatus,
    ExperimentExecutionPlan,
    RunIngestContract,
)


def test_run_ingest_contract_rejects_observed_result_write() -> None:
    with pytest.raises(ValueError, match="must not write observed results"):
        RunIngestContract(
            route_id="route",
            writes_observed_result=True,
        )


def test_experiment_execution_plan_rejects_execution_flags() -> None:
    contract = RunIngestContract(route_id="route")

    with pytest.raises(ValueError, match="cannot execute or write observed results"):
        ExperimentExecutionPlan(
            plan_id="plan",
            route_id="route",
            goal="test goal",
            status=ExecutionPlanStatus.PLANNED,
            ingest_contract=contract,
            automatically_executes=True,
        )


def test_experiment_execution_plan_rejects_ready_with_blockers() -> None:
    contract = RunIngestContract(route_id="route")

    with pytest.raises(ValueError, match="ready plan cannot have blockers"):
        ExperimentExecutionPlan(
            plan_id="plan",
            route_id="route",
            goal="test goal",
            status=ExecutionPlanStatus.READY_FOR_HUMAN_RUN,
            ingest_contract=contract,
            blockers=["missing-artifacts"],
        )
