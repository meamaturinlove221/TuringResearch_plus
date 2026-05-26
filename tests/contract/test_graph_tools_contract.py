from turing_research_plus.semantic_graph.models import CitationGraphExpandInput, GraphDirection
from turing_research_plus.semantic_graph.tools import (
    graph_author,
    graph_author_network,
    graph_author_papers,
    graph_citation_graph_expand,
    graph_citations,
    graph_paper_batch,
    graph_paper_lookup,
    graph_recommendations,
    graph_references,
)


def test_graph_tools_contract_exposes_expected_wrappers() -> None:
    wrappers = [
        graph_paper_lookup,
        graph_paper_batch,
        graph_references,
        graph_citations,
        graph_recommendations,
        graph_author,
        graph_author_papers,
        graph_citation_graph_expand,
        graph_author_network,
    ]

    assert [wrapper.__name__ for wrapper in wrappers] == [
        "graph_paper_lookup",
        "graph_paper_batch",
        "graph_references",
        "graph_citations",
        "graph_recommendations",
        "graph_author",
        "graph_author_papers",
        "graph_citation_graph_expand",
        "graph_author_network",
    ]


def test_graph_citation_graph_contract_defaults() -> None:
    request = CitationGraphExpandInput(seed_paper_ids=["p1"])

    assert request.direction == GraphDirection.BOTH
    assert request.depth_limit == 1
    assert request.max_nodes == 50
