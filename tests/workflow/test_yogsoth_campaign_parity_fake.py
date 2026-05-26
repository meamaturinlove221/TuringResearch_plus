from __future__ import annotations

from turing_research_plus.campaigns import (
    build_campaign_execution_plan,
    build_campaign_strategy_book,
    evaluate_campaign_preconditions,
)


def test_yogsoth_campaign_parity_fake_flow_is_route_only() -> None:
    book = build_campaign_strategy_book()
    preconditions = evaluate_campaign_preconditions(
        "knowledge_acquisition",
        provided_inputs=["source list", "source hygiene boundary"],
    )
    plan = build_campaign_execution_plan(
        "Collect literature and web source context for a paper survey",
        provided_inputs=["source list", "source hygiene boundary"],
    )

    assert book.does_not_execute is True
    assert book.by_campaign_id()["knowledge_acquisition"].primary_skill == (
        "turingresearch-fusion-literature-survey"
    )
    assert preconditions.ready_for_planning is True
    assert plan.campaign_id == "knowledge_acquisition"
    assert plan.does_not_execute is True
    assert plan.does_not_call_llm is True
    assert plan.does_not_use_network is True
    assert plan.replaces_master_orchestrator is False
    assert plan.ready_for_execution is False
