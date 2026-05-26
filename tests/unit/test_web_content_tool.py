from __future__ import annotations

from turing_research_plus.web import WebFetchingToolRequest, run_web_fetching_tool
from turing_research_plus.web.web_content_tool import (
    render_web_content_usage,
    web_content_from_fetch_result,
)


def test_web_content_tool_converts_fetch_result_to_review_context() -> None:
    fetched = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-page")
    ).fetch_result
    content = web_content_from_fetch_result(fetched)

    assert content.url == fetched.url
    assert content.human_verified is False
    assert content.requires_human_review is True
    assert content.content_hash == fetched.content_hash
    assert content.cache_key == fetched.cache_key
    assert content.text_content is not None


def test_render_web_content_usage_mentions_review_boundary() -> None:
    fetched = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-page")
    ).fetch_result
    rendered = render_web_content_usage(web_content_from_fetch_result(fetched))

    assert "Human verified: `false`" in rendered
    assert "Requires human review: `true`" in rendered
