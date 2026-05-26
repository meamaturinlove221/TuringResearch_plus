from turing_research_plus.semantic_graph.models import (
    AuthorNetworkInput,
    AuthorNode,
    GraphStatus,
    PaperNode,
)
from turing_research_plus.semantic_graph.service import SemanticGraphService


class FakeAuthorAdapter:
    def __init__(self) -> None:
        self.authors = {
            "a1": AuthorNode(author_id="a1", name="Author One", paper_ids=["p1"]),
            "a2": AuthorNode(author_id="a2", name="Author Two", paper_ids=["p1", "p2"]),
            "a3": AuthorNode(author_id="a3", name="Author Three", paper_ids=["p2"]),
        }
        self.papers = {
            "p1": PaperNode(paper_id="p1", title="Paper One", authors=["a1", "a2"]),
            "p2": PaperNode(paper_id="p2", title="Paper Two", authors=["a2", "a3"]),
        }

    def paper_lookup(self, paper_id: str) -> PaperNode | None:
        return self.papers.get(paper_id)

    def paper_batch(self, paper_ids: list[str]) -> list[PaperNode]:
        return [self.papers[paper_id] for paper_id in paper_ids if paper_id in self.papers]

    def references(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        return []

    def citations(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        return []

    def recommendations(self, paper_ids: list[str], limit: int = 10) -> list[PaperNode]:
        return []

    def author(self, author_id: str) -> AuthorNode | None:
        return self.authors.get(author_id)

    def author_papers(self, author_id: str) -> list[PaperNode]:
        author = self.authors.get(author_id)
        if author is None:
            return []
        return [self.papers[paper_id] for paper_id in author.paper_ids]


def test_author_lookup_and_author_papers() -> None:
    service = SemanticGraphService(FakeAuthorAdapter())

    author = service.author_by_id("a1")
    papers = service.papers_by_author("a1")

    assert author.status == GraphStatus.OK
    assert author.author is not None
    assert author.author.name == "Author One"
    assert [paper.paper_id for paper in papers.papers] == ["p1"]


def test_author_network_expands_coauthors() -> None:
    result = SemanticGraphService(FakeAuthorAdapter()).author_network(
        AuthorNetworkInput(seed_author_ids=["a1"], max_depth=2, max_authors=10)
    )

    assert result.status == GraphStatus.OK
    assert {author.author_id for author in result.authors} == {"a1", "a2", "a3"}
    edge_pairs = {(edge.source_author_id, edge.target_author_id) for edge in result.edges}
    assert ("a1", "a2") in edge_pairs
    assert ("a2", "a3") in edge_pairs


def test_author_network_respects_max_authors_with_frontier() -> None:
    result = SemanticGraphService(FakeAuthorAdapter()).author_network(
        AuthorNetworkInput(seed_author_ids=["a1"], max_depth=2, max_authors=1)
    )

    assert {author.author_id for author in result.authors} == {"a1"}
    assert {author.author_id for author in result.frontier_authors} == {"a2"}
