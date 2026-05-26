from __future__ import annotations

from turing_research_plus.scholar_tools import (
    build_scholar_full_tool_surface,
    render_scholar_full_tool_surface,
)


def test_scholar_full_tool_surface_lists_required_tools() -> None:
    surface = build_scholar_full_tool_surface()
    names = {tool.tool_name for tool in surface.tools}

    assert names == {
        "scholar.paper_searching",
        "scholar.paper_content",
        "scholar.paper_reference",
        "scholar.paper_reading",
    }
    assert surface.fake_mode_default is True
    assert surface.live_tests_skipped_by_default is True
    assert surface.mineru_enabled is False
    assert surface.automatic_full_paper_download is False
    assert surface.paywall_bypass_allowed is False
    assert surface.final_paper_conclusion_allowed is False
    assert surface.release_blocker is False


def test_render_scholar_full_tool_surface_mentions_boundaries() -> None:
    rendered = render_scholar_full_tool_surface(build_scholar_full_tool_surface())

    assert "`scholar.paper_searching`" in rendered
    assert "`scholar.paper_content`" in rendered
    assert "Fake mode default: `true`" in rendered
    assert "MinerU enabled: `false`" in rendered
    assert "Automatic full paper download: `false`" in rendered
