"""Deterministic fake adapters for tests and dry-runs."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from turing_research_plus.adapters.models import (
    ArxivQuery,
    ArxivSearchResult,
    LLMCompletionRequest,
    LLMCompletionResult,
    PDFConversionRequest,
    PDFConversionResult,
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


def _source(provider: str, source_id: str | None = None, url: str | None = None) -> SourceMetadata:
    return SourceMetadata(
        provider=provider,
        source_id=source_id,
        url=url,
        retrieval_time=datetime(2026, 5, 20, tzinfo=UTC),
        human_verified=False,
    )


class FakeSemanticScholarAdapter:
    """Fake Semantic Scholar adapter with deterministic paper lookup."""

    def paper_lookup(self, request: SemanticScholarPaperLookup) -> SemanticScholarPaperResult:
        paper = {
            "paper_id": "fake-semantic-scholar-001",
            "title": f"Fake result for {request.query}",
            "authors": ["TuringResearch Fake Adapter"],
            "year": 2026,
        }
        return SemanticScholarPaperResult(
            papers=[paper][: request.limit],
            source_metadata=[_source("semantic_scholar", "fake-semantic-scholar-001")],
        )

    def paper_lookup_by_id(
        self, request: SemanticScholarPaperIdLookup
    ) -> SemanticScholarPaperResult:
        paper = self._paper(request.paper_id, f"Fake paper {request.paper_id}")
        return SemanticScholarPaperResult(
            papers=[paper],
            source_metadata=[_source("semantic_scholar", request.paper_id)],
        )

    def paper_batch(self, request: SemanticScholarPaperBatchLookup) -> SemanticScholarPaperResult:
        papers = [self._paper(paper_id, f"Fake paper {paper_id}") for paper_id in request.paper_ids]
        return SemanticScholarPaperResult(
            papers=papers,
            source_metadata=[_source("semantic_scholar", "fake-batch")],
        )

    def references(self, request: SemanticScholarPaperListLookup) -> SemanticScholarPaperResult:
        papers = [
            self._paper(f"{request.paper_id}-ref-{index}", f"Fake reference {index}")
            for index in range(1, request.limit + 1)
        ]
        return SemanticScholarPaperResult(
            papers=papers,
            source_metadata=[_source("semantic_scholar", request.paper_id)],
        )

    def citations(self, request: SemanticScholarPaperListLookup) -> SemanticScholarPaperResult:
        papers = [
            self._paper(f"{request.paper_id}-cite-{index}", f"Fake citation {index}")
            for index in range(1, request.limit + 1)
        ]
        return SemanticScholarPaperResult(
            papers=papers,
            source_metadata=[_source("semantic_scholar", request.paper_id)],
        )

    def recommendations(
        self, request: SemanticScholarRecommendationLookup
    ) -> SemanticScholarPaperResult:
        seed = request.paper_ids[0]
        papers = [
            self._paper(f"{seed}-rec-{index}", f"Fake recommendation {index}")
            for index in range(1, request.limit + 1)
        ]
        return SemanticScholarPaperResult(
            papers=papers,
            source_metadata=[_source("semantic_scholar", seed)],
        )

    def author(self, request: SemanticScholarAuthorLookup) -> SemanticScholarAuthorResult:
        return SemanticScholarAuthorResult(
            authors=[
                {
                    "authorId": request.author_id,
                    "name": f"Fake author {request.author_id}",
                    "paperCount": 1,
                }
            ],
            source_metadata=[_source("semantic_scholar", request.author_id)],
        )

    def _paper(self, paper_id: str, title: str) -> dict[str, object]:
        return {
            "paper_id": paper_id,
            "paperId": paper_id,
            "title": title,
            "authors": ["TuringResearch Fake Adapter"],
            "year": 2026,
            "citationCount": 0,
            "isOpenAccess": False,
        }


class FakeArxivAdapter:
    """Fake arXiv adapter with deterministic search output."""

    def search(self, request: ArxivQuery) -> ArxivSearchResult:
        paper = {
            "arxiv_id": "0000.00000",
            "title": f"Fake arXiv result for {request.query}",
            "summary": "Fake adapter output for dry-run tests.",
        }
        return ArxivSearchResult(
            papers=[paper][: request.max_results],
            source_metadata=[_source("arxiv", "0000.00000")],
        )


class FakeWebSearchAdapter:
    """Fake public web search adapter."""

    def search(self, request: WebSearchRequest) -> WebSearchResult:
        result = {
            "title": f"Fake web result for {request.query}",
            "url": "https://example.com/fake-search-result",
            "snippet": "Fake adapter output; not human verified.",
        }
        return WebSearchResult(
            results=[result][: request.limit],
            source_metadata=[_source("web_search", url="https://example.com/fake-search-result")],
        )


class FakeWebFetchAdapter:
    """Fake public web fetch adapter."""

    def fetch(self, request: WebFetchRequest) -> WebFetchResult:
        url = str(request.url)
        return WebFetchResult(
            url=url,
            markdown=f"# Fake fetch\n\nFetched `{url}` in fake mode.",
            evidence=[{"type": "fake_fetch", "url": url}],
            source_metadata=[_source("web_fetch", url=url)],
        )


class FakeApifyWebAdapter(FakeWebFetchAdapter):
    """Backward-compatible fake Apify web adapter alias."""


class FakeOpenAICompatibleLLMAdapter:
    """Fake OpenAI-compatible LLM adapter."""

    def complete(self, request: LLMCompletionRequest) -> LLMCompletionResult:
        return LLMCompletionResult(
            text=f"Fake completion for: {request.prompt[:80]}",
            model=request.model,
            source_metadata=[_source("openai_compatible", request.model)],
        )


class FakePDFConverterAdapter:
    """Fake PDF converter adapter."""

    def convert(self, request: PDFConversionRequest) -> PDFConversionResult:
        output_dir = request.output_dir or Path(".")
        markdown_path = output_dir / f"{request.pdf_path.stem}.md"
        return PDFConversionResult(
            markdown_path=markdown_path,
            assets=[],
            page_map_path=output_dir / f"{request.pdf_path.stem}.page_map.json",
            converter_used="fake_pdf_converter",
            source_metadata=[_source("pdf_converter", str(request.pdf_path))],
        )
