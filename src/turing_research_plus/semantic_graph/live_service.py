"""Semantic graph bridge for optional Semantic Scholar live adapters."""

from __future__ import annotations

from typing import Any

from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import (
    SemanticScholarPaperBatchLookup,
    SemanticScholarPaperIdLookup,
    SemanticScholarPaperListLookup,
    SemanticScholarPaperLookup,
    SemanticScholarPaperResult,
    SemanticScholarRecommendationLookup,
)
from turing_research_plus.adapters.protocols import SemanticScholarAdapter
from turing_research_plus.semantic_graph.models import (
    GraphError,
    GraphErrorCode,
    GraphStatus,
    PaperBatchOutput,
    PaperListOutput,
    PaperLookupOutput,
    PaperNode,
    RecommendationOutput,
)


class SemanticScholarLiveGraphService:
    """Expose Semantic Scholar adapter results through semantic graph models."""

    def __init__(self, adapter: SemanticScholarAdapter | None = None) -> None:
        self.adapter = adapter or FakeSemanticScholarAdapter()

    def paper_lookup_by_title(self, query: str, limit: int = 1) -> PaperListOutput:
        result = self.adapter.paper_lookup(SemanticScholarPaperLookup(query=query, limit=limit))
        return self._list_output(result)

    def paper_lookup_by_id(self, paper_id: str) -> PaperLookupOutput:
        result = self.adapter.paper_lookup_by_id(SemanticScholarPaperIdLookup(paper_id=paper_id))
        if result.error is not None:
            return PaperLookupOutput(status=GraphStatus.ERROR, error=self._graph_error(result))
        papers = self._nodes(result)
        if not papers:
            return PaperLookupOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.NOT_FOUND, message="paper not found"),
            )
        return PaperLookupOutput(status=GraphStatus.OK, paper=papers[0])

    def paper_batch(self, paper_ids: list[str]) -> PaperBatchOutput:
        result = self.adapter.paper_batch(SemanticScholarPaperBatchLookup(paper_ids=paper_ids))
        if result.error is not None:
            return PaperBatchOutput(status=GraphStatus.ERROR, errors=[self._graph_error(result)])
        return PaperBatchOutput(status=GraphStatus.OK, papers=self._nodes(result))

    def references(self, paper_id: str, limit: int = 20) -> PaperListOutput:
        result = self.adapter.references(
            SemanticScholarPaperListLookup(paper_id=paper_id, limit=limit)
        )
        return self._list_output(result)

    def citations(self, paper_id: str, limit: int = 20) -> PaperListOutput:
        result = self.adapter.citations(
            SemanticScholarPaperListLookup(paper_id=paper_id, limit=limit)
        )
        return self._list_output(result)

    def recommendations(self, paper_ids: list[str], limit: int = 10) -> RecommendationOutput:
        result = self.adapter.recommendations(
            SemanticScholarRecommendationLookup(paper_ids=paper_ids, limit=limit)
        )
        if result.error is not None:
            return RecommendationOutput(status=GraphStatus.ERROR, error=self._graph_error(result))
        return RecommendationOutput(status=GraphStatus.OK, papers=self._nodes(result))

    def _list_output(self, result: SemanticScholarPaperResult) -> PaperListOutput:
        if result.error is not None:
            return PaperListOutput(status=GraphStatus.ERROR, error=self._graph_error(result))
        return PaperListOutput(status=GraphStatus.OK, papers=self._nodes(result))

    def _nodes(self, result: SemanticScholarPaperResult) -> list[PaperNode]:
        return [self._paper_node(paper) for paper in result.papers if self._has_title(paper)]

    def _paper_node(self, paper: dict[str, object]) -> PaperNode:
        paper_id = str(
            paper.get("paperId") or paper.get("paper_id") or paper.get("id") or "unknown"
        )
        title = str(paper.get("title") or "Untitled paper")
        authors = self._authors(paper.get("authors"))
        return PaperNode(
            paper_id=paper_id,
            title=title,
            year=self._int_or_none(paper.get("year")),
            citation_count=max(self._int_or_none(paper.get("citationCount")) or 0, 0),
            is_open_access=bool(paper.get("isOpenAccess") or paper.get("is_open_access") or False),
            authors=authors,
            abstract=str(paper["abstract"]) if paper.get("abstract") else None,
            metadata={
                "provider": "semantic_scholar",
                "retrieval_status": "retrieved",
                "human_verified": False,
                "url": paper.get("url"),
            },
        )

    def _authors(self, authors: object) -> list[str]:
        if not isinstance(authors, list):
            return []
        names: list[str] = []
        for author in authors:
            if isinstance(author, str):
                names.append(author)
            elif isinstance(author, dict) and author.get("name"):
                names.append(str(author["name"]))
        return names

    def _has_title(self, paper: dict[str, object]) -> bool:
        return bool(paper.get("title"))

    def _int_or_none(self, value: Any) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _graph_error(self, result: SemanticScholarPaperResult) -> GraphError:
        message = result.error.message if result.error else "Semantic Scholar adapter failure"
        return GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=message)


__all__ = ["SemanticScholarLiveGraphService"]
