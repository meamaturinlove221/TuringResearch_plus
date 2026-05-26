from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.experiment_execution.artifact_requirements import (
    build_artifact_requirements,
)
from turing_research_plus.experiment_execution.models import ExecutionPlanStatus
from turing_research_plus.experiment_execution.plan_builder import (
    build_experiment_execution_plan,
)
from turing_research_plus.experiment_execution.runbook import (
    render_experiment_execution_runbook,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "experiment_execution" / "e2e_runbook_demo"


def _route() -> ExperimentRouteSpec:
    return ExperimentRouteSpec.model_validate_json(
        (DEMO / "route_dsl.json").read_text(encoding="utf-8")
    )


def test_experiment_runbook_e2e_demo_files_exist() -> None:
    expected = [
        DEMO / "README.md",
        DEMO / "experiment_intent.md",
        DEMO / "route_dsl.json",
        DEMO / "artifact_requirements.md",
        DEMO / "safe_runbook.md",
        DEMO / "ingest_expectations.json",
        DEMO / "e2e_summary.md",
        ROOT / "docs" / "experiment-runbook-e2e.md",
    ]

    for path in expected:
        assert path.exists(), path


def test_experiment_runbook_e2e_builds_route_from_intent() -> None:
    route = _route()

    assert route.route_id == "experiment-runbook-e2e"
    assert route.status.value == "planned"
    assert route.goal == "Plan a safe fake experiment review route."
    assert "demo fixture manifest" in route.allowed_inputs
    assert "claim experiment completion" in " ".join(route.forbidden_actions)
    assert "run GPU" in route.forbidden_actions
    assert "run Modal" in route.forbidden_actions
    assert "write observed result" in route.forbidden_actions
    assert len(route.stages) == 3
    assert route.stages[0].id == "intent"
    assert route.stages[-1].id == "ingest"


def test_experiment_runbook_e2e_extracts_artifact_requirements_and_hard_gates() -> None:
    route = _route()
    requirements = build_artifact_requirements(route)
    plan = build_experiment_execution_plan(route)

    descriptions = {item.description for item in requirements}
    assert "intent summary" in descriptions
    assert "route DSL" in descriptions
    assert "hard gate checklist" in descriptions
    assert "artifact requirement table" in descriptions
    assert "runbook markdown" in descriptions
    assert "ingest expectation contract" in descriptions
    assert "proposed evidence update draft" in descriptions
    assert all(item.requires_human_review for item in requirements)
    assert "no_automatic_execution" in plan.hard_gates
    assert "no_gpu" in plan.hard_gates
    assert "no_modal" in plan.hard_gates
    assert "proposed_evidence_only" in plan.hard_gates


def test_experiment_runbook_e2e_generates_safe_runbook_and_ingest_contract() -> None:
    route = _route()
    plan = build_experiment_execution_plan(route)
    runbook = render_experiment_execution_runbook(plan)
    ingest_expectations = json.loads(
        (DEMO / "ingest_expectations.json").read_text(encoding="utf-8")
    )

    assert plan.status == ExecutionPlanStatus.READY_FOR_HUMAN_RUN
    assert plan.blockers == []
    assert plan.requires_human_review is True
    assert plan.automatically_executes is False
    assert plan.remote_execution is False
    assert plan.modal_call is False
    assert plan.gpu_call is False
    assert plan.writes_observed_result is False
    assert plan.ingest_contract.proposed_evidence_only is True
    assert plan.ingest_contract.writes_observed_result is False

    assert "Human operator runs experiment outside TuringResearch" in runbook
    assert "Automatically executes: `false`" in runbook
    assert "Modal call: `false`" in runbook
    assert "GPU call: `false`" in runbook
    assert "Writes observed result: `false`" in runbook

    assert ingest_expectations["route_id"] == route.route_id
    assert ingest_expectations["proposed_evidence_only"] is True
    assert ingest_expectations["writes_observed_result"] is False
    assert "hard_gate_results" in ingest_expectations["required_metadata"]
    assert "proposed evidence update draft" in ingest_expectations["required_artifacts"]


def test_experiment_runbook_e2e_static_outputs_match_runtime() -> None:
    route = _route()
    plan = build_experiment_execution_plan(route)
    runbook = render_experiment_execution_runbook(plan)
    static_runbook = (DEMO / "safe_runbook.md").read_text(encoding="utf-8")
    static_artifacts = (DEMO / "artifact_requirements.md").read_text(encoding="utf-8")
    summary = (DEMO / "e2e_summary.md").read_text(encoding="utf-8")

    for term in [
        "Safe Experiment Execution Runbook: experiment-runbook-e2e",
        "Status: `ready-for-human-run`",
        "Automatically executes: `false`",
        "Remote execution: `false`",
        "Modal call: `false`",
        "GPU call: `false`",
        "Writes observed result: `false`",
        "Proposed evidence only: `true`",
    ]:
        assert term in runbook
        assert term in static_runbook

    for requirement in plan.artifact_requirements:
        assert requirement.description in static_artifacts
        assert requirement.description in static_runbook

    assert "experiment intent -> route DSL -> hard gates" in summary
    assert "runbook -> ingest expectations" in summary


def test_experiment_runbook_e2e_docs_preserve_safety_boundaries() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            DEMO / "README.md",
            DEMO / "e2e_summary.md",
            ROOT / "docs" / "experiment-runbook-e2e.md",
        ]
    )

    required = [
        "fake/demo only",
        "no automatic experiment execution",
        "no GPU",
        "no Modal",
        "no observed result write",
        "only generates runbook and ingest contract",
        "human review required",
    ]
    for item in required:
        assert item in combined

    assert ("Tuling" + "Research") not in combined
    assert ("D:" + "/vggt") not in combined
    assert ("local_project_links" + ".yaml") not in combined
    assert ('"status": "' + 'observed"') not in combined
