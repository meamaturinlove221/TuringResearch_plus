from __future__ import annotations

from turing_research_plus.scholar_pipeline import (
    build_scholar_mcp_usage_guide,
    render_scholar_mcp_usage_guide,
)


def test_scholar_mcp_usage_guide_matches_example_config_style() -> None:
    guide = build_scholar_mcp_usage_guide()

    assert guide.server_name == "turingresearch-plus"
    assert guide.command == "turingresearch-plus-mcp"
    assert guide.args == ["--manifest"]
    assert guide.mode_env == "TURINGRESEARCH_MODE=fake"
    assert guide.live_tests_env == "TURINGRESEARCH_ENABLE_LIVE_TESTS=0"
    assert guide.semantic_scholar_live_env == "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0"
    assert guide.requires_human_review is True


def test_render_scholar_mcp_usage_guide_mentions_private_live_opt_in() -> None:
    rendered = render_scholar_mcp_usage_guide(build_scholar_mcp_usage_guide())

    assert "Server name: `turingresearch-plus`" in rendered
    assert (
        "Semantic Scholar live adapter: `TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0`"
        in rendered
    )
    assert "Live provider access is opt-in" in rendered
