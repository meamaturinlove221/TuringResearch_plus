"""Semantic graph service facade."""

from __future__ import annotations

from collections.abc import Callable

from tuling_research_plus.semantic_graph.author_graph import AuthorGraphBuilder
from tuling_research_plus.semantic_graph.citation_graph import CitationGraphBuilder
from tuling_research_plus.semantic_graph.client import (
    EmptySemanticGraphAdapter,
    SemanticGraphAdapter,
    SemanticGraphAdapterError,
)
from tuling_research_plus.semantic_graph.models import (
    AuthorInput,
    AuthorNetworkInput,
    AuthorNetworkOutput,
    AuthorOutput,
    AuthorPapersOutput,
    CitationGraphExpandInput,
    CitationGraphOutput,
    GraphError,
    GraphErrorCode,
    GraphStatus,
    PaperBatchInput,
    PaperBatchOutput,
    PaperListInput,
    PaperListOutput,
    PaperLookupInput,
    PaperLookupOutput,
    PaperNode,
    RecommendationInput,
    RecommendationOutput,
)


class SemanticGraphService:
    """Service facade for graph.* tools."""

    def __init__(self, adapter: SemanticGraphAdapter | None = None) -> None:
        self.adapter = adapter or EmptySemanticGraphAdapter()

    def paper_lookup(self, request: PaperLookupInput) -> PaperLookupOutput:
        try:
            paper = self.adapter.paper_lookup(request.paper_id)
        except SemanticGraphAdapterError as exc:
            return self._paper_error(str(exc))
        if paper is None:
            return PaperLookupOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.NOT_FOUND, message="paper not found"),
            )
        return PaperLookupOutput(status=GraphStatus.OK, paper=paper)

    def paper_lookup_by_id(self, paper_id: str) -> PaperLookupOutput:
        """Convenience wrapper for graph.paper_lookup."""

        return self.paper_lookup(PaperLookupInput(paper_id=paper_id))

    def paper_batch(self, request: PaperBatchInput) -> PaperBatchOutput:
        try:
            papers = self.adapter.paper_batch(request.paper_ids)
        except SemanticGraphAdapterError as exc:
            return PaperBatchOutput(
                status=GraphStatus.ERROR,
                errors=[
                    GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
                ],
            )
        return PaperBatchOutput(status=GraphStatus.OK, papers=papers)

    def paper_batch_by_ids(self, paper_ids: list[str]) -> PaperBatchOutput:
        """Convenience wrapper for graph.paper_batch."""

        return self.paper_batch(PaperBatchInput(paper_ids=paper_ids))

    def references(self, request: PaperListInput) -> PaperListOutput:
        return self._paper_list(lambda: self.adapter.references(request.paper_id, request.limit))

    def references_for_paper(self, paper_id: str, limit: int = 20) -> PaperListOutput:
        """Convenience wrapper for graph.references."""

        return self.references(PaperListInput(paper_id=paper_id, limit=limit))

    def citations(self, request: PaperListInput) -> PaperListOutput:
        return self._paper_list(lambda: self.adapter.citations(request.paper_id, request.limit))

    def citations_for_paper(self, paper_id: str, limit: int = 20) -> PaperListOutput:
        """Convenience wrapper for graph.citations."""

        return self.citations(PaperListInput(paper_id=paper_id, limit=limit))

    def recommendations(self, request: RecommendationInput) -> RecommendationOutput:
        try:
            papers = self.adapter.recommendations(request.paper_ids, request.limit)
        except SemanticGraphAdapterError as exc:
            return RecommendationOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
            )
        return RecommendationOutput(status=GraphStatus.OK, papers=papers)

    def author(self, request: AuthorInput) -> AuthorOutput:
        try:
            author = self.adapter.author(request.author_id)
        except SemanticGraphAdapterError as exc:
            return AuthorOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
            )
        if author is None:
            return AuthorOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.NOT_FOUND, message="author not found"),
            )
        return AuthorOutput(status=GraphStatus.OK, author=author)

    def author_by_id(self, author_id: str) -> AuthorOutput:
        """Convenience wrapper for graph.author."""

        return self.author(AuthorInput(author_id=author_id))

    def author_papers(self, request: AuthorInput) -> AuthorPapersOutput:
        try:
            papers = self.adapter.author_papers(request.author_id)
        except SemanticGraphAdapterError as exc:
            return AuthorPapersOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
            )
        return AuthorPapersOutput(status=GraphStatus.OK, papers=papers)

    def papers_by_author(self, author_id: str) -> AuthorPapersOutput:
        """Convenience wrapper for graph.author_papers."""

        return self.author_papers(AuthorInput(author_id=author_id))

    def citation_graph_expand(self, request: CitationGraphExpandInput) -> CitationGraphOutput:
        try:
            return CitationGraphBuilder(self.adapter).expand(request)
        except SemanticGraphAdapterError as exc:
            return CitationGraphOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
            )

    def author_network(self, request: AuthorNetworkInput) -> AuthorNetworkOutput:
        try:
            return AuthorGraphBuilder(self.adapter).expand(request)
        except SemanticGraphAdapterError as exc:
            return AuthorNetworkOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
            )

    def _paper_error(self, message: str) -> PaperLookupOutput:
        return PaperLookupOutput(
            status=GraphStatus.ERROR,
            error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=message),
        )

    def _paper_list(self, getter: Callable[[], list[PaperNode]]) -> PaperListOutput:
        try:
            papers = getter()
        except SemanticGraphAdapterError as exc:
            return PaperListOutput(
                status=GraphStatus.ERROR,
                error=GraphError(code=GraphErrorCode.ADAPTER_FAILURE, message=str(exc)),
            )
        return PaperListOutput(status=GraphStatus.OK, papers=papers)
