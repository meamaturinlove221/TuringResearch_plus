"""Live adapter protocols for TuringResearch Plus.

Protocols are interface contracts only. This module performs no network calls.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from turing_research_plus.adapters.errors import AdapterError, AdapterErrorCode
from turing_research_plus.adapters.models import (
    AdapterCachePolicy,
    AdapterRequestContext,
    AdapterRetryPolicy,
    AdapterTimeoutPolicy,
    ArxivQuery,
    ArxivSearchResult,
    LLMCompletionRequest,
    LLMCompletionResult,
    PDFConversionRequest,
    PDFConversionResult,
    RateLimitPolicy,
    SemanticScholarAuthorLookup,
    SemanticScholarAuthorResult,
    SemanticScholarPaperBatchLookup,
    SemanticScholarPaperIdLookup,
    SemanticScholarPaperListLookup,
    SemanticScholarPaperLookup,
    SemanticScholarPaperResult,
    SemanticScholarRecommendationLookup,
    SourceMetadata,
    WebFetchRequest,
    WebFetchResult,
    WebSearchRequest,
    WebSearchResult,
)


@runtime_checkable
class SemanticScholarAdapter(Protocol):
    """Protocol for optional Semantic Scholar live or fake adapters."""

    def paper_lookup(self, request: SemanticScholarPaperLookup) -> SemanticScholarPaperResult:
        """Look up papers through a live or fake Semantic Scholar adapter."""

    def paper_lookup_by_id(
        self, request: SemanticScholarPaperIdLookup
    ) -> SemanticScholarPaperResult:
        """Look up one paper by Semantic Scholar paper id."""

    def paper_batch(self, request: SemanticScholarPaperBatchLookup) -> SemanticScholarPaperResult:
        """Look up multiple papers by Semantic Scholar paper ids."""

    def references(self, request: SemanticScholarPaperListLookup) -> SemanticScholarPaperResult:
        """Return backward references for one paper."""

    def citations(self, request: SemanticScholarPaperListLookup) -> SemanticScholarPaperResult:
        """Return forward citations for one paper."""

    def recommendations(
        self, request: SemanticScholarRecommendationLookup
    ) -> SemanticScholarPaperResult:
        """Return optional recommendations for seed papers."""

    def author(self, request: SemanticScholarAuthorLookup) -> SemanticScholarAuthorResult:
        """Return optional author metadata."""


@runtime_checkable
class ArxivAdapter(Protocol):
    """Protocol for optional arXiv live or fake adapters."""

    def search(self, request: ArxivQuery) -> ArxivSearchResult:
        """Search arXiv through a live or fake adapter."""


@runtime_checkable
class WebSearchAdapter(Protocol):
    """Protocol for optional public web search adapters."""

    def search(self, request: WebSearchRequest) -> WebSearchResult:
        """Search public web metadata through a live or fake adapter."""


@runtime_checkable
class WebFetchAdapter(Protocol):
    """Protocol for optional public web fetch adapters."""

    def fetch(self, request: WebFetchRequest) -> WebFetchResult:
        """Fetch public web content through a live or fake adapter."""


@runtime_checkable
class OpenAICompatibleLLMAdapter(Protocol):
    """Protocol for optional OpenAI-compatible LLM live or fake adapters."""

    def complete(self, request: LLMCompletionRequest) -> LLMCompletionResult:
        """Run a completion through a live or fake LLM adapter."""


@runtime_checkable
class PDFConverterAdapter(Protocol):
    """Protocol for replaceable local PDF converter adapters."""

    def convert(self, request: PDFConversionRequest) -> PDFConversionResult:
        """Convert PDF input through a local or fake converter adapter."""


class ApifyWebAdapter(WebFetchAdapter, Protocol):
    """Backward-compatible alias for older Apify web fetch protocol naming."""


__all__ = [
    "AdapterCachePolicy",
    "AdapterError",
    "AdapterErrorCode",
    "AdapterRequestContext",
    "AdapterRetryPolicy",
    "AdapterTimeoutPolicy",
    "ApifyWebAdapter",
    "ArxivAdapter",
    "ArxivQuery",
    "ArxivSearchResult",
    "LLMCompletionRequest",
    "LLMCompletionResult",
    "OpenAICompatibleLLMAdapter",
    "PDFConversionRequest",
    "PDFConversionResult",
    "PDFConverterAdapter",
    "RateLimitPolicy",
    "SemanticScholarAuthorLookup",
    "SemanticScholarAuthorResult",
    "SemanticScholarAdapter",
    "SemanticScholarPaperBatchLookup",
    "SemanticScholarPaperIdLookup",
    "SemanticScholarPaperListLookup",
    "SemanticScholarPaperLookup",
    "SemanticScholarPaperResult",
    "SemanticScholarRecommendationLookup",
    "SourceMetadata",
    "WebFetchAdapter",
    "WebFetchRequest",
    "WebFetchResult",
    "WebSearchAdapter",
    "WebSearchRequest",
    "WebSearchResult",
]
