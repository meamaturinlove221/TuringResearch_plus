from __future__ import annotations

from turing_research_plus.citation_graph.expander import CitationGraphExpander
from turing_research_plus.citation_graph.models import (
    CitationGraphFilters,
    CitationGraphNode,
    CitationGraphRequest,
    CitationGraphRetrievalStatus,
    CitationGraphSourceAdapter,
)


def test_fake_expander_builds_vggt_related_work_graph() -> None:
    graph = CitationGraphExpander().fake_vggt_related_work_graph()

    assert graph.graph_id == "fake-vggt-related-work"
    assert graph.retrieval_status == CitationGraphRetrievalStatus.FAKE
    assert graph.nodes
    assert graph.edges
    assert graph.requires_human_review is True


def test_manual_seed_list_uses_manual_status_without_network() -> None:
    request = CitationGraphRequest(
        graph_id="manual",
        seed_papers=[CitationGraphNode(paper_id="P1", title="Manual seed", year=2020)],
        source_adapter=CitationGraphSourceAdapter.MANUAL,
    )

    graph = CitationGraphExpander().expand(request)

    assert graph.retrieval_status == CitationGraphRetrievalStatus.MANUAL
    assert graph.nodes[0].paper_id == "P1"
    assert "Manual graph only" in graph.limitations[0]


def test_year_filter_excludes_old_seed() -> None:
    request = CitationGraphRequest(
        graph_id="filtered",
        seed_papers=[CitationGraphNode(paper_id="old", title="Old", year=1999)],
        filters=CitationGraphFilters(min_year=2020),
        source_adapter=CitationGraphSourceAdapter.FAKE,
    )

    graph = CitationGraphExpander().expand(request)

    assert all((node.year or 0) >= 2020 for node in graph.nodes)
