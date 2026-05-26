from __future__ import annotations

from turing_research_plus.scholar_pipeline import (
    ScholarSourcePriority,
    build_scholar_source_priority_plan,
    render_scholar_source_priority_plan,
)


def test_scholar_source_priority_prefers_cached_markdown() -> None:
    plan = build_scholar_source_priority_plan()

    assert plan.priority[0] == ScholarSourcePriority.CACHED_MARKDOWN
    assert plan.priority[1] == ScholarSourcePriority.ARXIV
    assert plan.priority[2] == ScholarSourcePriority.SEMANTIC_SCHOLAR
    assert plan.live_enabled_by_default is False
    assert plan.automatic_full_paper_download is False
    assert plan.paywall_bypass_allowed is False
    assert plan.release_blocker is False


def test_render_scholar_source_priority_mentions_human_review() -> None:
    rendered = render_scholar_source_priority_plan(build_scholar_source_priority_plan())

    assert "`cached_markdown`" in rendered
    assert "Requires human review: `true`" in rendered
    assert "Automatic full paper download: `false`" in rendered
