from __future__ import annotations

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.wiki_export import (
    build_wiki_vault_export,
    render_wiki_vault_export,
)


def test_wiki_vault_export_builds_pages_backlinks_and_quality_reports() -> None:
    graph = VaultGraph(
        graph_id="wiki-vault",
        nodes=[
            build_concept_node("vggt", "VGGT"),
            build_concept_node("human-prior", "Human/Prior"),
            build_concept_node("claim", "Claim Node"),
        ],
        edges=[
            build_edge("human-prior", "vggt", VaultGraphEdgeType.RELATED_TO),
            build_edge("claim", "vggt", VaultGraphEdgeType.SUPPORTS),
            build_edge("claim", "missing-artifact", VaultGraphEdgeType.RELATED_TO),
        ],
    )

    export = build_wiki_vault_export(graph)

    assert export.requires_human_review is True
    assert "VGGT" in export.pages
    assert "Human-Prior" in export.pages
    assert "[[Claim Node]]" in export.pages["VGGT"]
    assert "missing-artifact" in export.backlink_index.dangling_targets
    assert export.dangling_link_report.release_blocker is True
    assert export.edge_quality_report.missing_edges == ["claim->vggt:supports"]
    assert export.graph_summary["nodes"] == 3

    markdown = render_wiki_vault_export(export)
    assert "Pages: `3`" in markdown
    assert "Dangling links: `1`" in markdown
    assert "[[VGGT]]" in markdown
