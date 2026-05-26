"""Semantic graph adapter protocol."""

from __future__ import annotations

from typing import Protocol

from turing_research_plus.semantic_graph.models import AuthorNode, PaperNode


class SemanticGraphAdapterError(RuntimeError):
    """Raised when a semantic graph adapter fails."""


class SemanticGraphAdapter(Protocol):
    """Adapter boundary for external paper graph services."""

    def paper_lookup(self, paper_id: str) -> PaperNode | None: ...

    def paper_batch(self, paper_ids: list[str]) -> list[PaperNode]: ...

    def references(self, paper_id: str, limit: int = 20) -> list[PaperNode]: ...

    def citations(self, paper_id: str, limit: int = 20) -> list[PaperNode]: ...

    def recommendations(self, paper_ids: list[str], limit: int = 10) -> list[PaperNode]: ...

    def author(self, author_id: str) -> AuthorNode | None: ...

    def author_papers(self, author_id: str) -> list[PaperNode]: ...


class EmptySemanticGraphAdapter:
    """Default no-network adapter that returns empty results."""

    def paper_lookup(self, paper_id: str) -> PaperNode | None:
        return None

    def paper_batch(self, paper_ids: list[str]) -> list[PaperNode]:
        return []

    def references(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        return []

    def citations(self, paper_id: str, limit: int = 20) -> list[PaperNode]:
        return []

    def recommendations(self, paper_ids: list[str], limit: int = 10) -> list[PaperNode]:
        return []

    def author(self, author_id: str) -> AuthorNode | None:
        return None

    def author_papers(self, author_id: str) -> list[PaperNode]:
        return []
