"""Web cache review helpers for the v1.3 tool surface."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.web.content_cache import WebContentCache


class WebCacheSurfaceReport(BaseModel):
    """Review report for cache status."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "web.cache"
    url: str = Field(min_length=1)
    cache_key: str = Field(min_length=64, max_length=64)
    status: str = Field(min_length=1)
    persistent_storage: bool = False
    stores_cookies: bool = False
    contains_private_content: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe cache behavior is present."""

        return (
            self.persistent_storage
            or self.stores_cookies
            or self.contains_private_content
            or not self.requires_human_review
        )


def inspect_web_cache(url: str, *, cache: WebContentCache | None = None) -> WebCacheSurfaceReport:
    """Inspect process-local cache status for a URL."""

    current_cache = cache or WebContentCache()
    return WebCacheSurfaceReport(
        url=url,
        cache_key=current_cache.key_for_url(url),
        status=current_cache.cache_status(url),
        persistent_storage=False,
        stores_cookies=False,
        contains_private_content=False,
        requires_human_review=True,
    )
