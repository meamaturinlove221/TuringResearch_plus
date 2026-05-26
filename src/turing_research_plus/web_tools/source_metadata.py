"""Source metadata surface for public web tool outputs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.web.models import SourceType
from turing_research_plus.web.source_metadata import (
    build_cache_key,
    build_source_metadata,
)


class WebSourceMetadataSurfaceReport(BaseModel):
    """Review-oriented web source metadata report."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "web.source_metadata"
    source_url: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    source_hygiene_status: str = Field(min_length=1)
    cache_key: str = Field(min_length=64, max_length=64)
    content_hash: str = Field(min_length=64, max_length=64)
    human_verified: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether metadata overstates verification."""

        return self.human_verified or not self.requires_human_review


def build_web_source_metadata_report(
    *,
    source_url: str,
    content: str,
    source_type: SourceType = SourceType.PUBLIC_WEB,
    source_hygiene_status: str = "public_or_authorized",
) -> WebSourceMetadataSurfaceReport:
    """Build source metadata for review without marking it verified."""

    metadata = build_source_metadata(
        source_url=source_url,
        content=content,
        provider="web_fetch",
        source_type=source_type,
        source_hygiene_status=source_hygiene_status,
    )
    return WebSourceMetadataSurfaceReport(
        source_url=metadata.source_url,
        provider=metadata.provider,
        source_type=metadata.source_type.value,
        source_hygiene_status=metadata.source_hygiene_status,
        cache_key=build_cache_key(source_url),
        content_hash=metadata.content_hash,
        human_verified=metadata.human_verified,
        requires_human_review=True,
    )
