from __future__ import annotations

from turing_research_plus.campaigns.router import route_campaign


def test_campaign_router_recommends_public_release_campaign() -> None:
    decision = route_campaign("Prepare public launch release candidate and privacy gate")

    assert decision.recommended_campaign == "public_release"
    assert decision.recommended_skill == "turingresearch-qa-release"
    assert decision.does_not_execute is True
    assert decision.does_not_call_llm is True
    assert decision.does_not_use_network is True


def test_campaign_router_recommends_artifact_audit_campaign() -> None:
    decision = route_campaign("Audit artifact manifest and missing export files")

    assert decision.recommended_campaign == "artifact_audit"
    assert "turingresearch-cache-and-ledger" in decision.ranked_skills


def test_campaign_router_falls_back_to_north_star() -> None:
    decision = route_campaign("unclear vague task")

    assert decision.recommended_campaign == "north_star"
    assert decision.confidence == 0.25
