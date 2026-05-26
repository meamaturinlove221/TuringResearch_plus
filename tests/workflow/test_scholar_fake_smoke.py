from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.scholar_tools import (
    PaperContentToolRequest,
    PaperReferenceToolRequest,
    PaperSearchingToolRequest,
    run_paper_content_tool,
    run_paper_reference_tool,
    run_paper_searching_tool,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "scholar_demo"
SMOKE = DEMO / "live_smoke"
DOC = ROOT / "docs" / "scholar-optional-live-smoke.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_scholar_fake_smoke_files_are_public_safe() -> None:
    data = json.loads(_text(SMOKE / "fake_smoke_input.json"))
    combined = "\n".join(
        _text(path)
        for path in [
            DOC,
            SMOKE / "README.md",
            SMOKE / "fake_smoke_input.json",
            SMOKE / "expected_fake_smoke_report.md",
            SMOKE / "live_skip_report.md",
        ]
    )

    assert data["mode"] == "fake"
    assert data["requires_api_key"] is False
    assert data["live_mode_enabled"] is False
    assert data["paper_download_enabled"] is False
    assert data["citation_verified"] is False
    assert data["requires_human_review"] is True
    assert "no API key in repo" in combined
    assert "no paper download by default" in combined
    assert "no fake citation verified" in combined
    assert "SEMANTIC_SCHOLAR_API_KEY=<private local value>" in combined
    assert "sk-" not in combined
    assert "ghp_" not in combined
    assert "D:" + "/vggt" not in combined
    assert "D:" + "\\vggt" not in combined


def test_scholar_fake_smoke_tools_run_without_key() -> None:
    data = json.loads(_text(SMOKE / "fake_smoke_input.json"))
    cached = (SMOKE / data["cached_markdown"]).resolve()

    search = run_paper_searching_tool(
        PaperSearchingToolRequest(
            query=data["query"],
            paper_id=data["paper_id"],
            cached_markdown_path=cached,
        )
    )
    content = run_paper_content_tool(
        PaperContentToolRequest(
            paper_id=data["paper_id"],
            title="Fake Scholar Optional Live Smoke",
            cached_markdown_path=cached,
        )
    )
    references = run_paper_reference_tool(
        PaperReferenceToolRequest(cached_markdown=cached.read_text(encoding="utf-8"))
    )

    assert search.selected_source == "cached_markdown"
    assert search.no_real_api_key_required is True
    assert search.requires_human_review is True
    assert content.requires_human_review is True
    assert content.references_section_present is True
    assert references.requires_human_review is True
    assert references.references
    assert not search.release_blocker
    assert not content.release_blocker
    assert not references.release_blocker


def test_scholar_fake_smoke_docs_define_live_skip_policy() -> None:
    combined = "\n".join(
        [
            _text(DOC),
            _text(ROOT / "docs" / "scholar-live-optional-guide.md"),
            _text(ROOT / "docs" / "optional-live-safety-policy.md"),
            _text(SMOKE / "live_skip_report.md"),
        ]
    )

    assert "live skipped by default" in combined
    assert "live requires explicit env" in combined
    assert "TURINGRESEARCH_ENABLE_LIVE_TESTS=0" in combined
    assert "TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE=0" in combined
    assert "SEMANTIC_SCHOLAR_API_KEY=" in combined
    assert "no paywall bypass" in combined
    assert "no automatic Evidence Ledger write" in combined
    assert "fake citations are never verified citations" in combined
