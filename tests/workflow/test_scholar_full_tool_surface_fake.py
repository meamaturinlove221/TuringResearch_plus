from __future__ import annotations

from pathlib import Path

from turing_research_plus.scholar_tools import (
    PaperContentToolRequest,
    PaperReadingToolRequest,
    PaperReferenceToolRequest,
    PaperSearchingToolRequest,
    build_scholar_full_tool_surface,
    run_paper_content_tool,
    run_paper_reading_tool,
    run_paper_reference_tool,
    run_paper_searching_tool,
)


def test_scholar_full_tool_surface_fake_workflow(tmp_path: Path) -> None:
    cached = tmp_path / "cached_paper.md"
    cached.write_text(
        "# Cached Paper\n\nLocal review notes.\n\n## References\n- Cached Ref A\n",
        encoding="utf-8",
    )

    surface = build_scholar_full_tool_surface()
    search = run_paper_searching_tool(
        PaperSearchingToolRequest(
            query="cached paper",
            paper_id="cached-paper",
            cached_markdown_path=cached,
        )
    )
    content = run_paper_content_tool(
        PaperContentToolRequest(
            paper_id="cached-paper",
            title="Cached Paper",
            cached_markdown_path=cached,
        )
    )
    references = run_paper_reference_tool(
        PaperReferenceToolRequest(cached_markdown=cached.read_text(encoding="utf-8"))
    )
    reading = run_paper_reading_tool(
        PaperReadingToolRequest(paper_id="cached-paper", title="Cached Paper")
    )

    assert surface.release_blocker is False
    assert search.selected_source == "cached_markdown"
    assert content.references_section_present is True
    assert references.references[0]["title"] == "Cached Ref A"
    assert reading.final_conclusion_generated is False
    assert reading.camera_ready_text_generated is False
    assert all(
        result.requires_human_review
        for result in [search, content, references, reading]
    )
    assert all(
        not result.release_blocker for result in [search, content, references, reading]
    )


def test_scholar_full_tool_surface_fake_workflow_has_no_live_or_download_defaults() -> None:
    surface = build_scholar_full_tool_surface()

    assert surface.fake_mode_default is True
    assert surface.live_tests_skipped_by_default is True
    assert surface.mineru_enabled is False
    assert surface.automatic_full_paper_download is False
    assert surface.paywall_bypass_allowed is False
    assert surface.final_paper_conclusion_allowed is False
    assert all(not tool.requires_api_key for tool in surface.tools)
    assert all(not tool.automatic_full_paper_download for tool in surface.tools)
    assert all(not tool.mineru_enabled for tool in surface.tools)
    assert all(not tool.paywall_bypass_allowed for tool in surface.tools)
    assert all(not tool.final_conclusion_generated for tool in surface.tools)
