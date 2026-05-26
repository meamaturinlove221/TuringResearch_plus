from __future__ import annotations

from turing_research_plus.skills.router import DEFAULT_ROUTES, MASTER_SKILL, route_skill


def test_router_recommends_web_fetch_skill() -> None:
    decision = route_skill("Need web fetch for a public project page and README")

    assert decision.category == "web fetch"
    assert decision.recommended_skill == "turingresearch-core-reproduction"
    assert decision.does_not_execute is True


def test_router_recommends_related_work_skill() -> None:
    decision = route_skill("Generate related work positioning from collision risk")

    assert decision.category == "related work"
    assert decision.recommended_skill == "turingresearch-paper-writing-pipeline"
    assert "turingresearch-fusion-semantic-graph" in decision.ranked_skills


def test_router_falls_back_to_master_orchestrator() -> None:
    decision = route_skill("something fuzzy with no matching route")

    assert decision.category == "fallback"
    assert decision.recommended_skill == MASTER_SKILL
    assert decision.confidence < 0.5


def test_default_routes_cover_required_categories() -> None:
    categories = {route.category for route in DEFAULT_ROUTES}

    assert "upstream watch" in categories
    assert "VGGT dogfooding" in categories
    assert "ontology" in categories
