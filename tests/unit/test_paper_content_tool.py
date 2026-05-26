from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.scholar_tools import (
    PaperContentToolRequest,
    run_paper_content_tool,
)


def test_paper_content_tool_reads_cached_markdown(tmp_path: Path) -> None:
    markdown = tmp_path / "paper.md"
    markdown.write_text("# Paper\n\nBody\n\n## References\n- Ref A\n", encoding="utf-8")

    result = run_paper_content_tool(
        PaperContentToolRequest(
            paper_id="paper-1",
            title="Paper",
            cached_markdown_path=markdown,
        )
    )

    assert result.tool_name == "scholar.paper_content"
    assert result.cache_hit is True
    assert result.references_section_present is True
    assert result.live_enabled is False
    assert result.automatic_full_paper_download is False
    assert result.heavy_ocr_enabled is False
    assert result.mineru_enabled is False
    assert result.requires_human_review is True
    assert result.release_blocker is False


def test_paper_content_tool_rejects_live_download_and_ocr(tmp_path: Path) -> None:
    markdown = tmp_path / "paper.md"
    markdown.write_text("# Paper\n", encoding="utf-8")

    with pytest.raises(ValueError, match="cached local Markdown"):
        PaperContentToolRequest(
            paper_id="paper-1",
            title="Paper",
            cached_markdown_path=markdown,
            live_enabled=True,
        )
    with pytest.raises(ValueError, match="download full papers"):
        PaperContentToolRequest(
            paper_id="paper-1",
            title="Paper",
            cached_markdown_path=markdown,
            automatic_full_paper_download=True,
        )
    with pytest.raises(ValueError, match="heavy OCR"):
        PaperContentToolRequest(
            paper_id="paper-1",
            title="Paper",
            cached_markdown_path=markdown,
            heavy_ocr_enabled=True,
        )
