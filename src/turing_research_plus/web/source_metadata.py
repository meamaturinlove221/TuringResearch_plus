"""Source metadata and hash helpers for web adapters."""

from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from turing_research_plus.web.models import SourceType, WebSourceMetadata


def hash_text(value: str) -> str:
    """Return a sha256 hex digest for stable cache and content identity."""

    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_cache_key(url: str) -> str:
    """Build a stable cache key for a normalized URL string."""

    return hash_text(url.strip())


def build_source_metadata(
    *,
    source_url: str,
    content: str,
    provider: str = "web_fetch",
    source_type: SourceType = SourceType.PUBLIC_WEB,
    source_hygiene_status: str = "public_or_authorized",
    retrieval_time: datetime | None = None,
) -> WebSourceMetadata:
    """Create source metadata with human verification disabled by default."""

    return WebSourceMetadata(
        source_url=source_url,
        retrieval_time=retrieval_time or datetime.now(UTC),
        content_hash=hash_text(content),
        provider=provider,
        source_type=source_type,
        human_verified=False,
        source_hygiene_status=source_hygiene_status,
    )
