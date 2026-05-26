from __future__ import annotations

from turing_research_plus.campaigns.execution_plan import (
    build_campaign_execution_plan,
    render_campaign_execution_plan,
)


def test_execution_plan_routes_but_does_not_execute() -> None:
    plan = build_campaign_execution_plan(
        "Prepare public release privacy gate and launch report",
        provided_inputs=["passing tests", "public-safe docs", "privacy scan"],
    )

    assert plan.campaign_id == "public_release"
    assert plan.recommended_skill == "turingresearch-qa-release"
    assert plan.ready_for_execution is False
    assert plan.does_not_execute is True
    assert plan.does_not_call_llm is True
    assert plan.does_not_use_network is True
    assert plan.replaces_master_orchestrator is False
    assert plan.precondition_report.ready_for_planning is True


def test_execution_plan_keeps_missing_preconditions_visible() -> None:
    plan = build_campaign_execution_plan("Plan experiment execution route")

    assert plan.campaign_id == "experiment_planning"
    assert plan.ready_for_execution is False
    assert plan.precondition_report.missing_preconditions
    assert "review missing preconditions" in plan.next_steps


def test_render_execution_plan_mentions_non_execution_boundary() -> None:
    plan = build_campaign_execution_plan("stress test unsafe release claim")
    rendered = render_campaign_execution_plan(plan)

    assert "Ready for execution: `false`" in rendered
    assert "Does not execute: `true`" in rendered
    assert "Replaces master orchestrator: `false`" in rendered
