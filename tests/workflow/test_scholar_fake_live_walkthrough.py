from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.scholar_tools import (
    PaperContentToolRequest,
    PaperReadingToolRequest,
    PaperReferenceToolRequest,
    PaperSearchingToolRequest,
    run_paper_content_tool,
    run_paper_reading_tool,
    run_paper_reference_tool,
    run_paper_searching_tool,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "scholar_demo"


def test_scholar_fake_live_walkthrough_demo_files_are_public_safe() -> None:
    search = json.loads((DEMO / "fake_paper_search.json").read_text(encoding="utf-8"))
    content = (DEMO / "fake_paper_content.md").read_text(encoding="utf-8")
    references = (DEMO / "fake_reference_report.md").read_text(encoding="utf-8")
    readme = (DEMO / "README.md").read_text(encoding="utf-8")

    assert search["mode"] == "fake"
    assert search["requires_api_key"] is False
    assert search["live_mode_enabled"] is False
    assert search["automatic_full_paper_download"] is False
    assert search["paywall_bypass_allowed"] is False
    assert search["requires_human_review"] is True
    assert search["papers"][0]["citation_verified"] is False
    assert search["papers"][0]["human_verified"] is False
    assert "not a downloaded paper" in content
    assert "Verified: false" in references
    assert "no paper download" in readme


def test_scholar_fake_live_walkthrough_tools_run_without_key() -> None:
    cached = DEMO / "fake_paper_content.md"

    search = run_paper_searching_tool(
        PaperSearchingToolRequest(
            query="Fake Scholar Demo Paper",
            paper_id="fake-scholar-demo-001",
            cached_markdown_path=cached,
        )
    )
    content = run_paper_content_tool(
        PaperContentToolRequest(
            paper_id="fake-scholar-demo-001",
            title="Fake Scholar Demo Paper",
            cached_markdown_path=cached,
        )
    )
    references = run_paper_reference_tool(
        PaperReferenceToolRequest(cached_markdown=cached.read_text(encoding="utf-8"))
    )
    reading = run_paper_reading_tool(
        PaperReadingToolRequest(
            paper_id="fake-scholar-demo-001",
            title="Fake Scholar Demo Paper",
        )
    )

    assert search.selected_source == "cached_markdown"
    assert search.no_real_api_key_required is True
    assert content.references_section_present is True
    assert references.references
    assert all("Verified:" not in item["title"] for item in references.references)
    assert reading.final_conclusion_generated is False
    assert reading.camera_ready_text_generated is False
    assert all(
        result.requires_human_review
        for result in [search, content, references, reading]
    )
    assert all(
        not result.release_blocker for result in [search, content, references, reading]
    )


def test_scholar_fake_live_walkthrough_docs_define_live_opt_in_only() -> None:
    docs = (ROOT / "docs" / "scholar-fake-live-walkthrough.md").read_text(
        encoding="utf-8"
    )

    assert "Fake mode is the default" in docs
    assert "Live mode is opt-in only" in docs
    assert "SEMANTIC_SCHOLAR_API_KEY=<private local value>" in docs
    assert "no automatic paper download" in docs
    assert "no paywall bypass" in docs
    assert "no fake citation is marked as verified" in docs


def test_scholar_fake_live_walkthrough_contains_no_secret_or_private_path() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in [
            ROOT / "docs" / "scholar-fake-live-walkthrough.md",
            DEMO / "README.md",
            DEMO / "fake_paper_search.json",
            DEMO / "fake_paper_content.md",
            DEMO / "fake_reference_report.md",
        ]
    )

    forbidden = ["D:/vggt", "D:\\vggt", "local_project_links.yaml", "ghp_"]
    for marker in forbidden:
        assert marker not in combined
    assert "sk-" not in combined
    assert "observed " + "success" not in combined.lower()
