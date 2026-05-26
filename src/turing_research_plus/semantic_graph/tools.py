"""Thin graph.* tool wrappers."""

from __future__ import annotations

from typing import Any

from tuling_research_plus.semantic_graph.client import SemanticGraphAdapter
from tuling_research_plus.semantic_graph.models import (
    AuthorInput,
    AuthorNetworkInput,
    CitationGraphExpandInput,
    PaperBatchInput,
    PaperListInput,
    PaperLookupInput,
    RecommendationInput,
)
from tuling_research_plus.semantic_graph.service import SemanticGraphService


def _service(adapter: SemanticGraphAdapter | None = None) -> SemanticGraphService:
    return SemanticGraphService(adapter)


def graph_paper_lookup(
    paper_id: str,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).paper_lookup(PaperLookupInput(paper_id=paper_id)).model_dump(
        mode="json"
    )


def graph_paper_batch(
    paper_ids: list[str],
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).paper_batch(PaperBatchInput(paper_ids=paper_ids)).model_dump(
        mode="json"
    )


def graph_references(
    paper_id: str,
    limit: int = 20,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).references(PaperListInput(paper_id=paper_id, limit=limit)).model_dump(
        mode="json"
    )


def graph_citations(
    paper_id: str,
    limit: int = 20,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).citations(PaperListInput(paper_id=paper_id, limit=limit)).model_dump(
        mode="json"
    )


def graph_recommendations(
    paper_ids: list[str],
    limit: int = 10,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).recommendations(
        RecommendationInput(paper_ids=paper_ids, limit=limit)
    ).model_dump(mode="json")


def graph_author(author_id: str, adapter: SemanticGraphAdapter | None = None) -> dict[str, Any]:
    return _service(adapter).author(AuthorInput(author_id=author_id)).model_dump(mode="json")


def graph_author_papers(
    author_id: str,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).author_papers(AuthorInput(author_id=author_id)).model_dump(mode="json")


def graph_citation_graph_expand(
    request: CitationGraphExpandInput,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).citation_graph_expand(request).model_dump(mode="json")


def graph_author_network(
    request: AuthorNetworkInput,
    adapter: SemanticGraphAdapter | None = None,
) -> dict[str, Any]:
    return _service(adapter).author_network(request).model_dump(mode="json")
