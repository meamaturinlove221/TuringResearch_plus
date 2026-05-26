"""Models for fake-first public web fetching."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RetrievalStatus(StrEnum):
    """Stable retrieval status labels."""

    RETRIEVED = "retrieved"
    CACHE_HIT = "cache-hit"
    DRY_RUN = "dry-run"
    LIVE_DISABLED = "live-disabled"
    SOURCE_BLOCKED = "source-blocked"
    ERROR = "error"


class SourceType(StrEnum):
    """Supported source types."""

    PUBLIC_WEB = "public_web"
    GITHUB_README = "github_readme"
    ARXIV_HTML = "arxiv_html"
    PROJECT_PAGE = "project_page"
    LOCAL_FIXTURE = "local_fixture"
    FAKE = "fake"


class WebSourceMetadata(BaseModel):
    """Source metadata carried by web fetch outputs."""

    model_config = ConfigDict(extra="forbid")

    source_url: str = Field(min_length=1)
    retrieval_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    content_hash: str = Field(min_length=64, max_length=64)
    provider: str = "web_fetch"
    source_type: SourceType = SourceType.PUBLIC_WEB
    human_verified: bool = False
    source_hygiene_status: str = "unknown"


class WebFetchRequest(BaseModel):
    """Input for public web fetch.

    `live_enabled` and `dry_run` deliberately default to the non-network path.
    """

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    source_type: SourceType = SourceType.PUBLIC_WEB
    fixture_path: Path | None = None
    dry_run: bool = True
    live_enabled: bool = False
    timeout_seconds: float = Field(default=20.0, gt=0)
    source_hygiene_status: str = "public_or_authorized"


class WebFetchResult(BaseModel):
    """Output for web fetch."""

    model_config = ConfigDict(extra="forbid")

    url: str
    retrieval_status: RetrievalStatus
    retrieval_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_type: SourceType
    content_type: str = "text/html"
    title: str | None = None
    text_content: str | None = None
    html_content: str | None = None
    content_hash: str = Field(min_length=64, max_length=64)
    cache_key: str = Field(min_length=64, max_length=64)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    source_metadata: WebSourceMetadata
    cache_hit: bool = False


class WebContentCacheRecord(BaseModel):
    """Cached web content plus provenance."""

    model_config = ConfigDict(extra="forbid")

    cache_key: str = Field(min_length=64, max_length=64)
    url: str = Field(min_length=1)
    retrieval_time: datetime
    content_hash: str = Field(min_length=64, max_length=64)
    source_metadata: WebSourceMetadata
    html_content: str | None = None
    text_content: str | None = None
    stale: bool = False
    manual_fixture_mode: bool = False
