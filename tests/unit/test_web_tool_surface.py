from __future__ import annotations

from turing_research_plus.web_tools import (
    build_web_full_tool_surface,
    render_web_full_tool_surface,
)


def test_web_full_tool_surface_lists_required_tools() -> None:
    surface = build_web_full_tool_surface()
    names = {tool.tool_name for tool in surface.tools}

    assert names == {
        "web.web_fetching",
        "web.web_content",
        "web.cache",
        "web.source_metadata",
        "web.apify_optional",
    }
    assert surface.fake_mode_default is True
    assert surface.live_tests_skipped_by_default is True
    assert surface.default_network is False
    assert surface.stores_cookies is False
    assert surface.paywall_bypass_allowed is False
    assert surface.private_content_fetching_allowed is False
    assert surface.automatic_evidence_promotion is False
    assert surface.release_blocker is False


def test_render_web_full_tool_surface_mentions_safety_boundaries() -> None:
    rendered = render_web_full_tool_surface(build_web_full_tool_surface())

    assert "`web.web_fetching`" in rendered
    assert "`web.web_content`" in rendered
    assert "`web.apify_optional`" in rendered
    assert "Default network: `false`" in rendered
    assert "Stores cookies: `false`" in rendered
    assert "Paywall bypass allowed: `false`" in rendered
