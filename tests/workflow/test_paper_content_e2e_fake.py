from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.markdown_export import (
    export_method_card_markdown,
)
from turing_research_plus.paper_method.models import (
    PaperMethodCardInput,
    PaperSourceType,
)
from turing_research_plus.scholar_tools import (
    PaperContentToolRequest,
    run_paper_content_tool,
)

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "scholar_demo" / "paper_content_e2e"


def test_paper_content_e2e_cached_markdown_to_method_card_input() -> None:
    cached_markdown = DEMO / "cached_paper.md"
    descriptor = json.loads((DEMO / "method_card_input.json").read_text("utf-8"))

    content = run_paper_content_tool(
        PaperContentToolRequest(
            paper_id=descriptor["paper_id"],
            title=descriptor["title"],
            cached_markdown_path=cached_markdown,
        )
    )

    assert content.tool_name == "scholar.paper_content"
    assert content.cache_hit is True
    assert content.references_section_present is True
    assert content.live_enabled is False
    assert content.automatic_full_paper_download is False
    assert content.heavy_ocr_enabled is False
    assert content.mineru_enabled is False
    assert content.release_blocker is False

    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id=content.paper_id,
            title=content.title,
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=Path(content.markdown_path),
            requires_real_paper_review=True,
        )
    )
    rendered = export_method_card_markdown(card)

    assert card.paper_id == "fake-paper-content-e2e"
    assert card.requires_human_review is True
    assert "cached Markdown note" in card.inputs
    assert "method-card input scaffold" in card.outputs
    assert "Cache-first workflow shape." in card.what_to_borrow
    assert "This fixture does not prove complete paper reading." in card.limitations
    assert "# Method Card: Cache-First Paper Content Fixture" in rendered


def test_paper_content_e2e_docs_keep_public_safety_boundary() -> None:
    combined = "\n".join(
        [
            (ROOT / "docs" / "paper-content-e2e.md").read_text("utf-8"),
            (DEMO / "README.md").read_text("utf-8"),
            (DEMO / "content_to_method_card_report.md").read_text("utf-8"),
        ]
    )

    for required in [
        "fake/default",
        "no automatic full paper download",
        "no paywall bypass",
        "no fake citation is marked as verified",
        "human review required",
    ]:
        assert required in combined

    for forbidden in [
        "D:/vggt",
        "D:\\vggt",
        "local_project_links.yaml",
        "ghp_",
        "sk-",
    ]:
        assert forbidden not in combined
