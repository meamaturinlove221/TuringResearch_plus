from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pptx_templates import (
    DECK_SECTION_TITLES,
    build_advisor_pptx_slides,
    render_pptx_review_markdown,
)


def _bundle(tmp_path: Path) -> AdvisorMarkdownBundle:
    source_files = {
        "advisor_report_source.md": (
            "# Advisor Report Source\n\n"
            "## Current Status\n\n"
            "Current status is review-only.\n\n"
            "## Boundary\n\n"
            "Planned work is not observed evidence.\n"
        ),
        "slides_outline.md": "# Slides Outline\n\n1. Research North Star\n",
        "figure_list.md": "# Figure List\n\nNo generated figures are included.\n",
        "table_list.md": "# Table List\n\nNo synthetic experiment table was generated.\n",
        "evidence_refs.md": "# Evidence Refs\n\nEvidence summary remains source-linked.\n",
        "limitations.md": "# Limitations\n\nRequires human review.\n",
        "next_actions.md": "# Next Actions\n\nCollect missing artifacts.\n",
        "manifest.yaml": "requires_human_review: true\n",
    }
    for filename, text in source_files.items():
        (tmp_path / filename).write_text(text, encoding="utf-8")
    return AdvisorMarkdownBundle(
        bundle_id="bundle-1",
        topic="VGGT Advisor",
        output_dir=str(tmp_path),
        files=[
            AdvisorBundleFile(path=str(tmp_path / filename), role=filename)
            for filename in source_files
        ],
    )


def test_pptx_template_contains_required_deck_sections(tmp_path: Path) -> None:
    slides = build_advisor_pptx_slides(_bundle(tmp_path))

    assert [slide.title for slide in slides] == DECK_SECTION_TITLES
    assert len(slides) == 8
    assert any("not-ready" in bullet for slide in slides for bullet in slide.bullets)


def test_pptx_review_markdown_preserves_boundaries(tmp_path: Path) -> None:
    markdown = render_pptx_review_markdown(_bundle(tmp_path))

    assert "## slide-01: Research North Star" in markdown
    assert "No fake figures, charts, or experiment values are generated" in markdown
    assert "Requires human review" in markdown
