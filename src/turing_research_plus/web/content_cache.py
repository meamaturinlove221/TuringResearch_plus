"""In-memory web content cache for tests and dry-runs."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from turing_research_plus.web.models import WebContentCacheRecord, WebFetchResult
from turing_research_plus.web.source_metadata import build_cache_key


@dataclass
class WebContentCache:
    """A small process-local cache used by fake/default workflows."""

    ttl_seconds: int | None = None
    entries: dict[str, WebContentCacheRecord] = field(default_factory=dict)

    def key_for_url(self, url: str) -> str:
        """Return a stable cache key for URL."""

        return build_cache_key(url)

    def get(self, url: str) -> WebContentCacheRecord | None:
        """Return a cache record or None."""

        key = self.key_for_url(url)
        record = self.entries.get(key)
        if record is None:
            return None
        if self.ttl_seconds is not None:
            cutoff = datetime.now(UTC) - timedelta(seconds=self.ttl_seconds)
            if record.retrieval_time < cutoff:
                record.stale = True
        return record

    def put_result(self, result: WebFetchResult, *, manual_fixture_mode: bool = False) -> None:
        """Cache a web fetch result."""

        self.entries[result.cache_key] = WebContentCacheRecord(
            cache_key=result.cache_key,
            url=result.url,
            retrieval_time=result.retrieval_time,
            content_hash=result.content_hash,
            source_metadata=result.source_metadata,
            html_content=result.html_content,
            text_content=result.text_content,
            stale=False,
            manual_fixture_mode=manual_fixture_mode,
        )

    def cache_status(self, url: str) -> str:
        """Return a compact hit/miss/stale status string."""

        record = self.get(url)
        if record is None:
            return "miss"
        return "stale" if record.stale else "hit"
