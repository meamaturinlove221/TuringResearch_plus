import pytest
from pydantic import ValidationError

from turing_research_plus.semantic_graph.models import (
    AuthorEdge,
    CitationGraphExpandInput,
    GraphDirection,
    PaperNode,
)


def test_paper_node_model_defaults() -> None:
    paper = PaperNode(paper_id="p1", title="Paper One")

    assert paper.citation_count == 0
    assert paper.authors == []
    assert paper.is_open_access is False


def test_citation_graph_input_validates_limits() -> None:
    with pytest.raises(ValidationError):
        CitationGraphExpandInput(
            seed_paper_ids=["p1"],
            direction=GraphDirection.BOTH,
            max_nodes=0,
        )


def test_author_edge_canonicalizes_pair() -> None:
    edge = AuthorEdge(source_author_id="z", target_author_id="a", shared_paper_ids=["p1"])

    assert edge.source_author_id == "a"
    assert edge.target_author_id == "z"
