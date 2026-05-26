"""Local-only web content service."""

from __future__ import annotations

from pathlib import Path

from turing_research.cache.keys import build_cache_key
from turing_research.cache.manager import CacheManager
from turing_research.errors import CoreError, ErrorCode
from turing_research.web.models import WebContentRequest, WebContentResult


class WebContentService:
    """Read web Markdown from the local cache only."""

    def __init__(self, cache_dir: str | Path) -> None:
        self.cache = CacheManager(Path(cache_dir) / "web_content")

    def get_content(self, request: WebContentRequest) -> WebContentResult:
        """Return cached Markdown for a URL."""

        key = build_cache_key("core.web_content", request.url)
        entry = self.cache.get(key)
        if entry is None:
            return WebContentResult(
                url=request.url,
                found=False,
                error=CoreError(
                    code=ErrorCode.CACHE_MISS,
                    message="web content is not available in local cache",
                ),
            )

        markdown = entry.value.get("markdown")
        if not isinstance(markdown, str):
            return WebContentResult(
                url=request.url,
                found=False,
                error=CoreError(
                    code=ErrorCode.INVALID_CACHE_ENTRY,
                    message="cached web content entry does not contain markdown",
                ),
            )

        return WebContentResult(
            url=request.url,
            found=True,
            markdown=markdown,
            metadata={str(key): str(value) for key, value in entry.metadata.items()},
        )
