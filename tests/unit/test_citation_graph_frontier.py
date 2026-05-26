from __future__ import annotations

from turing_research_plus.citation_graph.frontier import (
    frontier_report_markdown,
    select_frontier_nodes,
)
from turing_research_plus.citation_graph.models import (
    CitationGraph,
    CitationGraphNode,
    CitationGraphRetrievalStatus,
    CitationGraphSourceAdapter,
)


def test_frontier_excludes_seed_nodes() -> None:
    seed = CitationGraphNode(paper_id="seed", title="Seed")
    frontier = CitationGraphNode(
        paper_id="frontier",
        title="Frontier",
        year=2025,
        citation_count=50,
        topics=["VGGT"],
    )
    graph = CitationGraph(
        graph_id="g",
        seed_papers=[seed],
        nodes=[seed, frontier],
        source_adapter=CitationGraphSourceAdapter.FAKE,
        retrieval_status=CitationGraphRetrievalStatus.FAKE,
    )

    assert select_frontier_nodes(graph) == [frontier]


def test_frontier_report_renders_markdown() -> None:
    graph = CitationGraph(
        graph_id="g",
        seed_papers=[],
        nodes=[CitationGraphNode(paper_id="n", title="Node", topics=["VGGT"])],
        source_adapter=CitationGraphSourceAdapter.FAKE,
        retrieval_status=CitationGraphRetrievalStatus.FAKE,
    )

    markdown = frontier_report_markdown(graph)

    assert markdown.startswith("# Citation Frontier")
    assert "`n` Node" in markdown
