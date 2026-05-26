from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.figure_linker import (
    collect_mermaid_figure_links,
    render_figure_links_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS = ROOT / "examples" / "vggt-human-prior-survey" / "architecture_diagrams"


def test_collect_mermaid_figure_links_marks_review_only() -> None:
    links = collect_mermaid_figure_links(DIAGRAMS)

    assert {link.figure_id for link in links} == {
        "humanram_mapping",
        "modal_sparseconv_route",
        "neuralbody_mapping",
    }
    assert all(link.source_status == "derived-from-fixture" for link in links)
    assert all(link.requires_human_review for link in links)


def test_render_figure_links_markdown_does_not_fabricate_figures() -> None:
    markdown = render_figure_links_markdown(collect_mermaid_figure_links(DIAGRAMS))

    assert "# Method Figure Links" in markdown
    assert "not fabricated paper figures" in markdown
    assert "requires-human-review" in markdown
