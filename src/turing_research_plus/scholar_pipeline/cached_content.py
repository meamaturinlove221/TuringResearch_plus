"""Cached Markdown paper content helpers."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.adapters.models import SourceMetadata
from turing_research_plus.scholar_pipeline.models import CachedPaperContent


def read_cached_paper_content(
    *,
    paper_id: str,
    title: str,
    markdown_path: Path,
) -> CachedPaperContent:
    """Read cached local Markdown without downloading paper content."""

    markdown = markdown_path.read_text(encoding="utf-8-sig")
    return CachedPaperContent(
        paper_id=paper_id,
        title=title,
        markdown_path=str(markdown_path),
        markdown=markdown,
        cache_hit=True,
        source_metadata=[
            SourceMetadata(
                provider="cached_markdown",
                source_id=paper_id,
                url=str(markdown_path),
                human_verified=False,
            )
        ],
        requires_human_review=True,
    )


def cached_content_available(path: Path | None) -> bool:
    """Return whether cached Markdown can be read."""

    return path is not None and path.exists() and path.is_file()
