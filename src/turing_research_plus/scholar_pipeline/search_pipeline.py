"""Cache-first scholar search pipeline."""

from __future__ import annotations

from turing_research_plus.adapters.fake import FakeArxivAdapter, FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import (
    ArxivQuery,
    SemanticScholarPaperLookup,
    SourceMetadata,
)
from turing_research_plus.scholar_pipeline.cached_content import (
    cached_content_available,
    read_cached_paper_content,
)
from turing_research_plus.scholar_pipeline.models import (
    ScholarPipelineRequest,
    ScholarPipelineResult,
    ScholarPipelineStatus,
    ScholarSourcePriority,
)

SOURCE_PRIORITY = [
    ScholarSourcePriority.CACHED_MARKDOWN,
    ScholarSourcePriority.ARXIV,
    ScholarSourcePriority.SEMANTIC_SCHOLAR,
    ScholarSourcePriority.UNPAYWALL_PLACEHOLDER,
    ScholarSourcePriority.MANUAL,
]


def run_scholar_search_pipeline(
    request: ScholarPipelineRequest,
    *,
    arxiv_adapter: FakeArxivAdapter | None = None,
    semantic_scholar_adapter: FakeSemanticScholarAdapter | None = None,
) -> ScholarPipelineResult:
    """Run the source-priority paper lookup pipeline without default networking."""

    if cached_content_available(request.cached_markdown_path):
        cached = read_cached_paper_content(
            paper_id=request.paper_id or request.query,
            title=request.query,
            markdown_path=request.cached_markdown_path,  # type: ignore[arg-type]
        )
        return ScholarPipelineResult(
            query=request.query,
            source_priority=SOURCE_PRIORITY,
            selected_source=ScholarSourcePriority.CACHED_MARKDOWN,
            status=ScholarPipelineStatus.CACHE_HIT,
            papers=[{"paper_id": cached.paper_id, "title": cached.title, "source": "cache"}],
            cached_content=cached,
            source_metadata=cached.source_metadata,
            limitations=["Cached Markdown is not automatically human verified."],
            requires_human_review=True,
        )

    if request.known_arxiv_url:
        source = SourceMetadata(provider="arxiv", url=request.known_arxiv_url, human_verified=False)
        return ScholarPipelineResult(
            query=request.query,
            source_priority=SOURCE_PRIORITY,
            selected_source=ScholarSourcePriority.ARXIV,
            status=ScholarPipelineStatus.FAKE_RESULT,
            papers=[
                {
                    "paper_id": request.paper_id or request.known_arxiv_url,
                    "title": request.query,
                    "url": request.known_arxiv_url,
                    "source": "arxiv_url",
                }
            ],
            source_metadata=[source],
            limitations=["arXiv URL is metadata only; no full text was downloaded."],
            requires_human_review=True,
        )

    if request.dry_run or not request.live_enabled:
        arxiv = arxiv_adapter or FakeArxivAdapter()
        arxiv_result = arxiv.search(ArxivQuery(query=request.query, max_results=1))
        if arxiv_result.papers:
            return ScholarPipelineResult(
                query=request.query,
                source_priority=SOURCE_PRIORITY,
                selected_source=ScholarSourcePriority.ARXIV,
                status=ScholarPipelineStatus.FAKE_RESULT,
                papers=arxiv_result.papers,
                source_metadata=arxiv_result.source_metadata,
                limitations=[
                    "Fake arXiv adapter result for dry-run.",
                    "Live adapters are disabled by default.",
                ],
                requires_human_review=True,
            )
        semantic = semantic_scholar_adapter or FakeSemanticScholarAdapter()
        semantic_result = semantic.paper_lookup(
            SemanticScholarPaperLookup(query=request.query, limit=1)
        )
        return ScholarPipelineResult(
            query=request.query,
            source_priority=SOURCE_PRIORITY,
            selected_source=ScholarSourcePriority.SEMANTIC_SCHOLAR,
            status=ScholarPipelineStatus.FAKE_RESULT,
            papers=semantic_result.papers,
            source_metadata=semantic_result.source_metadata,
            limitations=["Fake Semantic Scholar adapter result for dry-run."],
            requires_human_review=True,
        )

    if request.manual_fallback:
        return ScholarPipelineResult(
            query=request.query,
            source_priority=SOURCE_PRIORITY,
            selected_source=ScholarSourcePriority.MANUAL,
            status=ScholarPipelineStatus.MANUAL_FALLBACK,
            papers=request.manual_fallback,
            limitations=["Manual fallback is not automatically human verified."],
            requires_human_review=True,
        )

    return ScholarPipelineResult(
        query=request.query,
        source_priority=SOURCE_PRIORITY,
        selected_source=ScholarSourcePriority.MANUAL,
        status=ScholarPipelineStatus.REQUIRES_HUMAN_REVIEW,
        papers=[],
        limitations=["No cached, arXiv, Semantic Scholar, Unpaywall, or manual source resolved."],
        requires_human_review=True,
    )
