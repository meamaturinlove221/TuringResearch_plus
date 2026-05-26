"""Local-only paper content service."""

from __future__ import annotations

from pathlib import Path

from tuling_research.cache.keys import build_cache_key
from tuling_research.cache.manager import CacheManager
from tuling_research.errors import CoreError, ErrorCode
from tuling_research.scholar.models import PaperContentRequest, PaperContentResult


class PaperContentService:
    """Read paper Markdown from the local cache only."""

    def __init__(self, cache_dir: str | Path) -> None:
        self.cache = CacheManager(Path(cache_dir) / "paper_content")

    def get_content(self, request: PaperContentRequest) -> PaperContentResult:
        """Return cached Markdown for a paper ID."""

        key = build_cache_key("core.paper_content", request.paper_id)
        entry = self.cache.get(key)
        if entry is None:
            return PaperContentResult(
                paper_id=request.paper_id,
                found=False,
                error=CoreError(
                    code=ErrorCode.CACHE_MISS,
                    message="paper content is not available in local cache",
                ),
            )

        markdown = entry.value.get("markdown")
        if not isinstance(markdown, str):
            return PaperContentResult(
                paper_id=request.paper_id,
                found=False,
                error=CoreError(
                    code=ErrorCode.INVALID_CACHE_ENTRY,
                    message="cached paper content entry does not contain markdown",
                ),
            )

        return PaperContentResult(
            paper_id=request.paper_id,
            found=True,
            markdown=markdown,
            metadata={str(key): str(value) for key, value in entry.metadata.items()},
        )
