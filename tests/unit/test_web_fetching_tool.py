from __future__ import annotations

from turing_research_plus.web import WebFetchingToolRequest, run_web_fetching_tool
from turing_research_plus.web.models import RetrievalStatus, SourceType
from turing_research_plus.web.web_fetching_tool import render_web_fetching_usage


def test_web_fetching_tool_defaults_to_dry_run_no_network() -> None:
    result = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-page")
    )

    assert result.tool_name == "web_fetching"
    assert result.default_network is False
    assert result.stores_cookies is False
    assert result.requires_api_key is False
    assert result.fetch_result.retrieval_status == RetrievalStatus.DRY_RUN
    assert result.fetch_result.source_type == SourceType.FAKE
    assert result.graceful_skip is True


def test_web_fetching_tool_blocks_private_source_hygiene() -> None:
    result = run_web_fetching_tool(
        WebFetchingToolRequest(
            url="https://example.com/private",
            source_hygiene_status="private",
        )
    )

    assert result.fetch_result.retrieval_status == RetrievalStatus.SOURCE_BLOCKED
    assert result.graceful_skip is True


def test_render_web_fetching_usage_mentions_safety_flags() -> None:
    result = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-page")
    )
    rendered = render_web_fetching_usage(result)

    assert "Default network: `false`" in rendered
    assert "Stores cookies: `false`" in rendered
    assert "Requires API key: `false`" in rendered
