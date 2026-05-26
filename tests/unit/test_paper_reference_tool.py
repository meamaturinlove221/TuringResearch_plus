from __future__ import annotations

from turing_research_plus.scholar_tools import (
    PaperReferenceToolRequest,
    run_paper_reference_tool,
)


def test_paper_reference_tool_uses_fake_semantic_scholar_by_id() -> None:
    result = run_paper_reference_tool(
        PaperReferenceToolRequest(paper_id="fake-paper-id", limit=3)
    )

    assert result.tool_name == "scholar.paper_reference"
    assert result.source == "semantic_scholar"
    assert len(result.references) == 3
    assert result.live_enabled is False
    assert result.paywall_bypass_allowed is False
    assert result.automatic_full_paper_download is False
    assert result.requires_human_review is True
    assert result.release_blocker is False


def test_paper_reference_tool_uses_cached_markdown_fallback() -> None:
    markdown = "# Paper\n\n## References\n- Cached Ref A\n- Cached Ref B\n"

    result = run_paper_reference_tool(PaperReferenceToolRequest(cached_markdown=markdown))

    assert result.source == "cached_markdown"
    assert result.fallback_used is True
    assert [item["title"] for item in result.references] == [
        "Cached Ref A",
        "Cached Ref B",
    ]
