from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pdf_templates import (
    PDF_REQUIRED_SECTIONS,
    build_pdf_section_text,
    render_pdf_review_markdown,
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
        "figure_list.md": "# Figure List\n\nNo generated figures are included.\n",
        "table_list.md": "# Table List\n\nNo synthetic experiment table was generated.\n",
        "evidence_refs.md": "# Evidence Refs\n\nEvidence summary remains source-linked.\n",
        "limitations.md": "# Limitations\n\nRequires human review.\n",
        "next_actions.md": "# Next Actions\n\nCollect missing artifacts.\n",
        "slides_outline.md": "# Slides Outline\n\nOutline only.\n",
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


def test_pdf_template_contains_required_sections(tmp_path: Path) -> None:
    sections = build_pdf_section_text(_bundle(tmp_path))

    assert set(PDF_REQUIRED_SECTIONS) <= set(sections)
    assert "review-only" in sections["current status"]
    assert "does not create visual evidence" in sections["visual readiness"]


def test_pdf_review_markdown_preserves_boundaries(tmp_path: Path) -> None:
    markdown = render_pdf_review_markdown(_bundle(tmp_path))

    assert "## Current Status" in markdown
    assert "No figures, result values, or experiment claims are fabricated" in markdown
    assert "Requires human review" in markdown
