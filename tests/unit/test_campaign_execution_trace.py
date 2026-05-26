from __future__ import annotations

from turing_research_plus.campaigns.execution_plan import build_campaign_execution_plan
from turing_research_plus.campaigns.execution_trace import (
    build_campaign_execution_trace,
    trace_from_plan,
)


def test_campaign_execution_trace_records_route_without_execution() -> None:
    trace = build_campaign_execution_trace(
        "Prepare public release privacy gate and launch report",
        provided_inputs=["passing tests", "public-safe docs", "privacy scan"],
    )

    assert trace.campaign_id == "public_release"
    assert trace.recommended_skill == "turingresearch-qa-release"
    assert trace.fake_trace is True
    assert trace.does_not_execute is True
    assert trace.does_not_call_llm is True
    assert trace.does_not_use_network is True
    assert trace.does_not_mutate_evidence_ledger is True
    assert trace.ready_for_execution is False
    assert trace.blocked is False
    assert {step.step_id for step in trace.steps} == {
        "route_campaign",
        "check_preconditions",
        "prepare_handoff",
        "record_proposed_outputs",
        "human_review_gate",
    }
    assert all(step.executed is False for step in trace.steps)
    assert all(step.called_tool is False for step in trace.steps)
    assert all(step.evidence_status == "proposed-only" for step in trace.steps)


def test_campaign_execution_trace_keeps_missing_preconditions_visible() -> None:
    trace = build_campaign_execution_trace("Plan experiment execution route")

    assert trace.campaign_id == "experiment_planning"
    assert trace.blocked is True
    assert trace.missing_preconditions
    assert any(
        step.status == "blocked_missing_preconditions"
        for step in trace.steps
        if step.step_id == "check_preconditions"
    )


def test_trace_from_plan_preserves_plan_route() -> None:
    plan = build_campaign_execution_plan(
        "stress test unsafe release claim",
        provided_inputs=["candidate claim or release surface"],
    )
    trace = trace_from_plan(plan)

    assert trace.campaign_id == plan.campaign_id
    assert trace.recommended_skill == plan.recommended_skill
    assert trace.confidence == plan.confidence
