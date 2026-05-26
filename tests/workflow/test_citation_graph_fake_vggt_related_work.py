from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.citation_graph.expander import CitationGraphExpander
from turing_research_plus.citation_graph.markdown_export import (
    citation_frontier_to_markdown,
    citation_graph_to_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE_DIR = ROOT / "examples" / "vggt-human-prior-survey" / "citation_graph"


def test_fake_vggt_related_work_graph_serializes_to_json_and_markdown() -> None:
    graph = CitationGraphExpander().fake_vggt_related_work_graph()

    payload = graph.model_dump(mode="json")
    markdown = citation_graph_to_markdown(graph)
    frontier = citation_frontier_to_markdown(graph)

    assert payload["retrieval_status"] == "fake"
    assert payload["requires_human_review"] is True
    assert "not a complete related work review" in " ".join(graph.limitations)
    assert "# Citation Graph" in markdown
    assert "# Citation Frontier" in frontier


def test_example_fixture_is_valid_json_placeholder() -> None:
    payload = json.loads((EXAMPLE_DIR / "fake_related_work_graph.json").read_text(encoding="utf-8"))

    assert payload["graph_id"] == "fake-vggt-related-work"
    assert payload["requires_human_review"] is True
