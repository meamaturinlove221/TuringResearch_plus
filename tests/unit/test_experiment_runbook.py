from __future__ import annotations

from turing_research_plus.experiment_execution.plan_builder import (
    build_experiment_execution_plan,
)
from turing_research_plus.experiment_execution.runbook import (
    render_experiment_execution_runbook,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec


def test_experiment_execution_runbook_renders_safety_flags() -> None:
    route = ExperimentRouteSpec(
        route_id="runbook-route",
        goal="Render safe runbook.",
        context="demo only",
        forbidden_actions=["claim experiment completion"],
        hard_gates=["no_promotion"],
        artifact_requirements=["run manifest"],
        stages=[
            {
                "id": "s1",
                "name": "Stage",
                "purpose": "Prepare.",
                "outputs": ["review artifact"],
                "hard_gates": ["artifact_required"],
            }
        ],
    )
    plan = build_experiment_execution_plan(route)

    markdown = render_experiment_execution_runbook(plan)

    assert "Automatically executes: `false`" in markdown
    assert "Remote execution: `false`" in markdown
    assert "Modal call: `false`" in markdown
    assert "GPU call: `false`" in markdown
    assert "Writes observed result: `false`" in markdown
    assert "Proposed evidence only: `true`" in markdown
