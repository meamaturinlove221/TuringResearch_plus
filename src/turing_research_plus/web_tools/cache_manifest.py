"""Review-only Web cache manifest helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.web.models import RetrievalStatus, SourceType, WebContentCacheRecord
from turing_research_plus.web.source_metadata import hash_text
from turing_research_plus.web_tools.url_normalization import normalize_url


class WebCacheLiveStatus(StrEnum):
    """Explicit fake/live status carried by cache manifest entries."""

    FAKE = "fake"
    LIVE = "live"
    CACHE_ONLY = "cache-only"


class WebCacheManifestEntry(BaseModel):
    """Manifest entry for one cached or cacheable Web source."""

    model_config = ConfigDict(extra="forbid")

    source_url: str = Field(min_length=1)
    normalized_url: str = Field(min_length=1)
    fetch_time: datetime
    content_hash: str = Field(min_length=64, max_length=64)
    cache_key: str = Field(min_length=64, max_length=64)
    retrieval_status: RetrievalStatus = RetrievalStatus.DRY_RUN
    live_status: WebCacheLiveStatus = WebCacheLiveStatus.FAKE
    source_type: SourceType = SourceType.PUBLIC_WEB
    provider: str = Field(default="web_fetch", min_length=1)
    human_verified: bool = False
    requires_human_review: bool = True
    network_used: bool = False
    stores_cookies: bool = False
    contains_private_content: bool = False
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_review_and_live_boundaries(self) -> Self:
        """Keep manifest entries review-only and honest about live use."""

        if not self.requires_human_review:
            raise ValueError("web cache manifest entries require human review")
        if self.human_verified:
            raise ValueError("web cache manifest entries are not human verified by default")
        if self.stores_cookies:
            raise ValueError("web cache manifest entries must not store cookies")
        if self.contains_private_content:
            raise ValueError("web cache manifest entries must not contain private content")
        if self.network_used and self.live_status != WebCacheLiveStatus.LIVE:
            raise ValueError("network_used requires live status")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether this entry violates public release cache boundaries."""

        return (
            self.stores_cookies
            or self.contains_private_content
            or self.human_verified
            or not self.requires_human_review
            or (self.network_used and self.live_status != WebCacheLiveStatus.LIVE)
        )


class WebCacheManifest(BaseModel):
    """Manifest for one or more Web cache entries."""

    model_config = ConfigDict(extra="forbid")

    manifest_version: str = "v1.4-web-cache-manifest"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    entries: list[WebCacheManifestEntry] = Field(default_factory=list)
    fake_mode_default: bool = True
    live_network_default: bool = False
    cookie_storage_enabled: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether any manifest-level or entry-level release blocker exists."""

        return (
            not self.fake_mode_default
            or self.live_network_default
            or self.cookie_storage_enabled
            or not self.requires_human_review
            or any(entry.release_blocker for entry in self.entries)
        )


def build_web_cache_manifest_entry(
    *,
    source_url: str,
    content: str,
    fetch_time: datetime | None = None,
    retrieval_status: RetrievalStatus = RetrievalStatus.DRY_RUN,
    live_status: WebCacheLiveStatus = WebCacheLiveStatus.FAKE,
    source_type: SourceType = SourceType.PUBLIC_WEB,
    provider: str = "web_fetch",
    network_used: bool = False,
    warnings: list[str] | None = None,
) -> WebCacheManifestEntry:
    """Build a manifest entry without fetching or trusting the source."""

    normalized = normalize_url(source_url)
    return WebCacheManifestEntry(
        source_url=source_url.strip(),
        normalized_url=normalized.normalized_url,
        fetch_time=fetch_time or datetime.now(UTC),
        content_hash=hash_text(content),
        cache_key=normalized.cache_key,
        retrieval_status=retrieval_status,
        live_status=live_status,
        source_type=source_type,
        provider=provider,
        network_used=network_used,
        warnings=warnings or [],
    )


def build_web_cache_manifest(
    entries: list[WebCacheManifestEntry],
) -> WebCacheManifest:
    """Build a review-only cache manifest."""

    return WebCacheManifest(entries=entries)


def manifest_entry_from_cache_record(record: WebContentCacheRecord) -> WebCacheManifestEntry:
    """Create a manifest entry from an existing process-local cache record."""

    return build_web_cache_manifest_entry(
        source_url=record.url,
        content=record.text_content or record.html_content or "",
        fetch_time=record.retrieval_time,
        retrieval_status=RetrievalStatus.CACHE_HIT if not record.stale else RetrievalStatus.DRY_RUN,
        live_status=WebCacheLiveStatus.CACHE_ONLY,
        source_type=record.source_metadata.source_type,
        provider=record.source_metadata.provider,
        network_used=False,
        warnings=["cache record is stale"] if record.stale else [],
    )
