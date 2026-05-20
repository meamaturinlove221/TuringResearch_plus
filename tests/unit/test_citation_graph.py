from tuling_research_plus.semantic_graph.client import SemanticGraphAdapterError
from tuling_research_plus.semantic_graph.models import (
    AuthorNode,
    CitationGraphExpandInput,
    GraphDirection,
    GraphErrorCode,
    GraphStatus,
    PaperNode,
)
from tuling_research_plus.semantic_graph.service import SemanticGraphService


class FakeSemanticScholarAdapter:
    def __init__(self, fail: bool = False) -> None:
        self.fail = fail
        self.papers = {
            "seed": PaperNode(
                paper_id="seed",
                title="Seed",
                year=2020,
                citation_count=10,
                is_open_access=True,
                authors=["a1"],
            ),
            "ref1": PaperNode(
                paper_id="ref1",
                title="Reference One",
                year=2019,
                citation_count=25,
                is_open_access=True,
                authors=["a1", "a2"],
            ),
            "ref2": PaperNode(
                paper_id="ref2",
                title="Reference Two",
                year=2010,
                citation_count=1,
                is_open_access=False,
                authors=["a3"],
            ),
            "cit1": PaperNode(
                paper_id="cit1",
                title="Citation One",
                year=2021,
                citation_count=5,
                is_open_access=True,
                authors=["a2"],
            ),
            "cit2": PaperNode(
                paper_id="cit2",
                title="Citation Two",
                year=2022,
                citation_count=30,
                is_open_access=True,
                authors=["a4"],
            ),
            "next": PaperNode(
                paper_id="next",
                title="Recommended Next",
                year=2023,
                citation_count=50,
                is_open_access=True,
                authors=["a5"],
            ),
        }
        self.refs = {"seed": ["ref1", "ref2"], "cit1": ["ref1"]}
        self.cits = {"seed": ["cit1", "cit2"], "ref1": ["seed", "cit1"]}

    def _fail_if_needed(self) -> None:
        if self.fail:
            raise SemanticGraphAdapterError("adapter failed")

    def paper_lookup(self, paper_id: str) -> PaperNode | None:
        self._fail_if_needed()
        return self.papers.get(paper_id)

    def paper_batch(self, paper_ids: list[str]) -> list[PaperNode]:
        self._fail_if_needed()
        return [self.papers[paper_id] for paper_id in paper_ids if paper_id in self.papers]

    def references(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        self._fail_if_needed()
        return [self.papers[paper_id] for paper_id in self.refs.get(paper_id, [])[:limit]]

    def citations(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        self._fail_if_needed()
        return [self.papers[paper_id] for paper_id in self.cits.get(paper_id, [])[:limit]]

    def recommendations(self, paper_ids: list[str], limit: int = 10) -> list[PaperNode]:
        self._fail_if_needed()
        return [self.papers["next"]][:limit]

    def author(self, author_id: str) -> AuthorNode | None:
        self._fail_if_needed()
        return None

    def author_papers(self, author_id: str) -> list[PaperNode]:
        self._fail_if_needed()
        return []


def test_single_paper_lookup() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter()).paper_lookup_by_id("seed")

    assert result.status == GraphStatus.OK
    assert result.paper is not None
    assert result.paper.title == "Seed"


def test_batch_lookup() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter()).paper_batch_by_ids(["seed", "ref1"])

    assert result.status == GraphStatus.OK
    assert [paper.paper_id for paper in result.papers] == ["seed", "ref1"]


def test_reference_and_citation_expansion() -> None:
    service = SemanticGraphService(FakeSemanticScholarAdapter())

    references = service.references_for_paper("seed")
    citations = service.citations_for_paper("seed")

    assert [paper.paper_id for paper in references.papers] == ["ref1", "ref2"]
    assert [paper.paper_id for paper in citations.papers] == ["cit1", "cit2"]


def test_citation_graph_supports_both_directions_and_duplicate_merge() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter()).citation_graph_expand(
        CitationGraphExpandInput(
            seed_paper_ids=["seed"],
            direction=GraphDirection.BOTH,
            depth_limit=2,
            max_nodes=10,
            recommendation_limit=1,
        )
    )

    assert result.status == GraphStatus.OK
    assert len({node.paper_id for node in result.nodes}) == len(result.nodes)
    assert "ref1" in {node.paper_id for node in result.nodes}
    assert "cit1" in {node.paper_id for node in result.nodes}
    assert result.recommended_next_reads[0].paper_id == "next"


def test_depth_limit_and_max_node_limit_create_frontier() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter()).citation_graph_expand(
        CitationGraphExpandInput(
            seed_paper_ids=["seed"],
            direction=GraphDirection.FORWARD,
            depth_limit=0,
            max_nodes=1,
        )
    )

    assert [node.paper_id for node in result.nodes] == ["seed"]
    assert [node.paper_id for node in result.frontier_nodes] == ["seed"]


def test_year_citation_and_open_access_filters() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter()).citation_graph_expand(
        CitationGraphExpandInput(
            seed_paper_ids=["seed"],
            direction=GraphDirection.BOTH,
            depth_limit=1,
            max_nodes=10,
            min_year=2018,
            min_citation_count=5,
            open_access_only=True,
        )
    )

    paper_ids = {node.paper_id for node in result.nodes}
    assert "ref1" in paper_ids
    assert "ref2" not in paper_ids


def test_empty_result() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter()).paper_lookup_by_id("missing")

    assert result.status == GraphStatus.ERROR
    assert result.error is not None
    assert result.error.code == GraphErrorCode.NOT_FOUND


def test_adapter_failure() -> None:
    result = SemanticGraphService(FakeSemanticScholarAdapter(fail=True)).paper_lookup_by_id("seed")

    assert result.status == GraphStatus.ERROR
    assert result.error is not None
    assert result.error.code == GraphErrorCode.ADAPTER_FAILURE
