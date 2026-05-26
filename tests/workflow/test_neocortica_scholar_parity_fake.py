from __future__ import annotations

from turing_research_plus.scholar_pipeline import (
    ScholarFallbackStatus,
    ScholarSourcePriority,
    build_scholar_fallback_policy,
    build_scholar_mcp_usage_guide,
    build_scholar_source_priority_plan,
    build_scholar_tool_list,
)


def test_neocortica_scholar_parity_fake_flow_is_public_safe() -> None:
    priority = build_scholar_source_priority_plan()
    tools = build_scholar_tool_list()
    guide = build_scholar_mcp_usage_guide()
    fallback = build_scholar_fallback_policy()
    fallback_by_source = {rule.source: rule for rule in fallback.rules}

    assert priority.priority[:3] == [
        ScholarSourcePriority.CACHED_MARKDOWN,
        ScholarSourcePriority.ARXIV,
        ScholarSourcePriority.SEMANTIC_SCHOLAR,
    ]
    assert priority.live_enabled_by_default is False
    assert tools.no_real_api_key_required is True
    assert guide.mode_env.endswith("fake")
    assert guide.live_tests_env.endswith("0")
    assert fallback_by_source["mineru_heavy_pdf_fallback"].status == ScholarFallbackStatus.DEFERRED
    assert fallback_by_source["paywall_bypass"].status == ScholarFallbackStatus.REJECTED
    assert fallback.final_paper_conclusion_allowed is False
    assert fallback.automatic_full_paper_download_allowed is False
