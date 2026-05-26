from __future__ import annotations

from turing_research_plus.campaigns.strategy_book import (
    CAMPAIGN_ALIASES,
    build_campaign_strategy_book,
    render_campaign_strategy_book,
)


def test_strategy_book_contains_required_yogsoth_campaigns_and_aliases() -> None:
    book = build_campaign_strategy_book()
    by_id = book.by_campaign_id()

    required = {
        "north_star",
        "knowledge_acquisition",
        "deep_insight",
        "hypothesis",
        "ideation",
        "convergence",
        "stress_test",
        "experiment_execution",
        "public_release",
    }

    assert required <= set(by_id)
    assert by_id["hypothesis"].campaign_id == CAMPAIGN_ALIASES["hypothesis"]
    assert by_id["ideation"].campaign_id == CAMPAIGN_ALIASES["ideation"]
    assert by_id["experiment_execution"].campaign_id == CAMPAIGN_ALIASES[
        "experiment_execution"
    ]
    assert book.does_not_execute is True
    assert book.does_not_call_llm is True
    assert book.does_not_use_network is True


def test_render_strategy_book_is_review_only() -> None:
    rendered = render_campaign_strategy_book()

    assert "# TuringResearch Strategy Book" in rendered
    assert "Does not execute: `true`" in rendered
    assert "`experiment_execution`" in rendered
    assert "`turingresearch-qa-release`" in rendered
