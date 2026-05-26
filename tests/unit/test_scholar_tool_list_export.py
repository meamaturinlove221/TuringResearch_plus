from __future__ import annotations

from turing_research_plus.scholar_pipeline import (
    build_scholar_tool_list,
    render_scholar_tool_list,
)


def test_scholar_tool_list_has_public_fake_default_tools() -> None:
    tool_list = build_scholar_tool_list()
    names = {tool.name for tool in tool_list.tools}

    assert "paper.search_pipeline" in names
    assert "paper.reference_pipeline" in names
    assert "paper.three_pass_reading_plan" in names
    assert tool_list.live_tests_skipped_by_default is True
    assert tool_list.no_real_api_key_required is True
    assert all(tool.requires_human_review for tool in tool_list.tools)
    assert all(not tool.requires_api_key for tool in tool_list.tools)


def test_render_scholar_tool_list_is_markdown_table() -> None:
    rendered = render_scholar_tool_list(build_scholar_tool_list())

    assert "| Tool | Purpose | Mode | API key | Human review |" in rendered
    assert "`paper.search_pipeline`" in rendered
    assert "No real API key required: `true`" in rendered
