"""Reference resolution pipeline with Semantic Scholar and Markdown fallback."""

from __future__ import annotations

import re

from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import SemanticScholarPaperListLookup
from turing_research_plus.scholar_pipeline.models import (
    PaperReference,
    ReferencePipelineRequest,
    ReferencePipelineResult,
    ReferenceSource,
)


def resolve_references(
    request: ReferencePipelineRequest,
    *,
    semantic_scholar_adapter: FakeSemanticScholarAdapter | None = None,
) -> ReferencePipelineResult:
    """Resolve references with SS primary, cached Markdown fallback, manual fallback."""

    if request.paper_id:
        adapter = semantic_scholar_adapter or FakeSemanticScholarAdapter()
        result = adapter.references(
            SemanticScholarPaperListLookup(paper_id=request.paper_id, limit=request.limit)
        )
        references = [
            PaperReference(
                reference_id=str(paper.get("paperId") or paper.get("paper_id") or index),
                title=str(paper.get("title") or "Untitled reference"),
                source=ReferenceSource.SEMANTIC_SCHOLAR,
                source_metadata=result.source_metadata,
                requires_human_review=True,
            )
            for index, paper in enumerate(result.papers, start=1)
        ]
        return ReferencePipelineResult(
            source=ReferenceSource.SEMANTIC_SCHOLAR,
            references=references,
            pagination_used=len(references) >= request.limit,
            fallback_used=False,
            limitations=["Semantic Scholar reference list is not human verified."],
            requires_human_review=True,
        )

    if request.cached_markdown:
        references = _references_from_markdown(request.cached_markdown)
        if references:
            return ReferencePipelineResult(
                source=ReferenceSource.CACHED_MARKDOWN,
                references=references,
                pagination_used=False,
                fallback_used=True,
                limitations=["References were parsed from cached Markdown heuristically."],
                requires_human_review=True,
            )

    if request.manual_references:
        return ReferencePipelineResult(
            source=ReferenceSource.MANUAL,
            references=[
                PaperReference(
                    reference_id=f"manual-{index}",
                    title=title,
                    source=ReferenceSource.MANUAL,
                    requires_human_review=True,
                )
                for index, title in enumerate(request.manual_references, start=1)
            ],
            fallback_used=True,
            limitations=["Manual references require human review."],
            requires_human_review=True,
        )

    return ReferencePipelineResult(
        source=ReferenceSource.UNKNOWN,
        references=[],
        fallback_used=True,
        limitations=["No references resolved; requires human review."],
        requires_human_review=True,
    )


def _references_from_markdown(markdown: str) -> list[PaperReference]:
    section = _references_section(markdown)
    if not section:
        return []
    references: list[PaperReference] = []
    for line in section.splitlines():
        stripped = line.strip()
        if not stripped or stripped.lower().startswith("#"):
            continue
        match = re.match(r"^[-*]\s+(?P<title>.+)$", stripped)
        if not match:
            match = re.match(r"^\[\d+\]\s*(?P<title>.+)$", stripped)
        if match:
            references.append(
                PaperReference(
                    reference_id=f"cached-ref-{len(references) + 1}",
                    title=match.group("title").strip(),
                    source=ReferenceSource.CACHED_MARKDOWN,
                    requires_human_review=True,
                )
            )
    return references


def _references_section(markdown: str) -> str | None:
    match = re.search(r"(?ims)^#+\s*references\s*$", markdown)
    if not match:
        return None
    return markdown[match.end() :]
