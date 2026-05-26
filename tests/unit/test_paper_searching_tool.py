from __future__ import annotations

import pytest

from turing_research_plus.scholar_tools import (
    PaperSearchingToolRequest,
    run_paper_searching_tool,
)


def test_paper_searching_tool_runs_fake_default_search() -> None:
    result = run_paper_searching_tool(
        PaperSearchingToolRequest(query="geometry-aware human reconstruction")
    )

    assert result.tool_name == "scholar.paper_searching"
    assert result.papers
    assert result.live_enabled is False
    assert result.no_real_api_key_required is True
    assert result.automatic_full_paper_download is False
    assert result.mineru_enabled is False
    assert result.paywall_bypass_allowed is False
    assert result.requires_human_review is True
    assert result.release_blocker is False


def test_paper_searching_tool_rejects_unsafe_options() -> None:
    with pytest.raises(ValueError, match="download full papers"):
        PaperSearchingToolRequest(
            query="paper",
            automatic_full_paper_download=True,
        )
    with pytest.raises(ValueError, match="MinerU"):
        PaperSearchingToolRequest(query="paper", mineru_enabled=True)
    with pytest.raises(ValueError, match="paywalls"):
        PaperSearchingToolRequest(query="paper", paywall_bypass_allowed=True)
