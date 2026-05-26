from __future__ import annotations

from turing_research_plus.citation_graph.models import (
    CitationGraph,
    CitationGraphEdge,
    CitationGraphEdgeType,
    CitationGraphNode,
    CitationGraphRetrievalStatus,
    CitationGraphSourceAdapter,
)


def test_citation_graph_dedupes_nodes_and_edges() -> None:
    node = CitationGraphNode(paper_id="P1", title="Seed")
    edge = CitationGraphEdge(
        source_id="P1",
        target_id="P2",
        edge_type=CitationGraphEdgeType.CITES,
    )

    graph = CitationGraph(
        graph_id="g1",
        seed_papers=[node],
        nodes=[node, node],
        edges=[edge, edge],
        source_adapter=CitationGraphSourceAdapter.MANUAL,
        retrieval_status=CitationGraphRetrievalStatus.MANUAL,
    )

    assert len(graph.nodes) == 1
    assert len(graph.edges) == 1
    assert graph.requires_human_review is True


def test_edge_type_values_are_stable() -> None:
    assert CitationGraphEdgeType.CITES == "cites"
    assert CitationGraphEdgeType.CITED_BY == "cited_by"
    assert CitationGraphEdgeType.MANUAL_RELATED == "manual_related"
