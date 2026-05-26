from __future__ import annotations

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.edge_quality import (
    evaluate_edge_quality,
    render_edge_quality_report,
)
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node


def test_edge_quality_reports_missing_weak_and_review_items() -> None:
    graph = VaultGraph(
        graph_id="edge-quality",
        nodes=[
            build_concept_node("claim", "Claim Node"),
            build_concept_node("method", "Method Node"),
        ],
        edges=[
            build_edge("claim", "method", VaultGraphEdgeType.SUPPORTS),
            build_edge(
                "method",
                "claim",
                VaultGraphEdgeType.RELATED_TO,
                source_refs=["demo"],
                confidence=0.2,
            ),
        ],
    )

    report = evaluate_edge_quality(graph)

    assert report.release_blocker is True
    assert report.missing_edges == ["claim->method:supports"]
    assert report.weak_edges == ["method->claim:related_to"]
    assert report.requires_review_nodes == ["claim", "method"]
    assert report.graph_summary["nodes"] == 2
    assert report.graph_summary["edges"] == 2

    markdown = render_edge_quality_report(report)
    assert "Vault Edge Quality" in markdown
    assert "`claim->method:supports`" in markdown
    assert "`method->claim:related_to`" in markdown
