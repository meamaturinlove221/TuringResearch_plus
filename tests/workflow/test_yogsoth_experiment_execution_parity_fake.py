from __future__ import annotations

from pathlib import Path

from turing_research_plus.experiment_execution.models import ExecutionPlanStatus
from turing_research_plus.experiment_execution.plan_builder import (
    build_experiment_execution_plan,
)
from turing_research_plus.experiment_execution.runbook import (
    render_experiment_execution_runbook,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec

ROOT = Path(__file__).resolve().parents[2]


def test_yogsoth_experiment_execution_parity_fake_workflow_is_plan_only() -> None:
    route = ExperimentRouteSpec(
        route_id="yogsoth-execution-parity",
        goal="Plan safe experiment execution parity.",
        context="fake/demo route only; no execution",
        forbidden_actions=[
            "claim experiment completion",
            "run Modal",
            "run GPU",
            "write observed result",
        ],
        hard_gates=["no_promotion", "real_backend_required"],
        artifact_requirements=["run manifest", "artifact index", "hard gate report"],
        stages=[
            {
                "id": "plan",
                "name": "Plan",
                "purpose": "Prepare human-run checklist.",
                "outputs": ["runbook"],
                "hard_gates": ["no_promotion"],
            },
            {
                "id": "ingest",
                "name": "Ingest",
                "purpose": "Ingest exported bundle after human run.",
                "outputs": ["proposed evidence updates"],
                "hard_gates": ["real_backend_required"],
            },
        ],
    )

    plan = build_experiment_execution_plan(route)
    markdown = render_experiment_execution_runbook(plan)

    assert plan.status == ExecutionPlanStatus.READY_FOR_HUMAN_RUN
    assert plan.automatically_executes is False
    assert plan.remote_execution is False
    assert plan.modal_call is False
    assert plan.gpu_call is False
    assert plan.writes_observed_result is False
    assert plan.ingest_contract.proposed_evidence_only is True
    assert plan.ingest_contract.writes_observed_result is False
    assert "Human operator runs experiment outside TuringResearch" in markdown
    assert "Writes observed result: `false`" in markdown


def test_yogsoth_experiment_execution_docs_and_contract_exist() -> None:
    expected_paths = [
        ROOT / "contracts" / "yogsoth_experiment_execution_parity.yaml",
        ROOT / "docs" / "yogsoth-experiment-execution-parity.md",
        ROOT / "docs" / "safe-experiment-execution-runbook.md",
    ]

    for path in expected_paths:
        assert path.exists(), path

    contract = (
        ROOT / "contracts" / "yogsoth_experiment_execution_parity.yaml"
    ).read_text(encoding="utf-8")
    assert "automatic_execution: false" in contract
    assert "writes_observed_result: false" in contract
