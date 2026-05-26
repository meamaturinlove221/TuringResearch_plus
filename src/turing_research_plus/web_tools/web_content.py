"""Operator-facing web content review surface."""

from __future__ import annotations

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.web import WebFetchingToolRequest, run_web_fetching_tool
from turing_research_plus.web.web_content_tool import (
    WebContentToolResult,
    web_content_from_fetch_result,
)


class WebContentSurfaceRequest(BaseModel):
    """Request for converting fetched content into review context."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)
    live_enabled: bool = False
    human_verified: bool = False
    promote_to_evidence: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_content_boundary(self) -> Self:
        if self.live_enabled:
            raise ValueError("web_content surface does not enable live fetch by default")
        if self.human_verified:
            raise ValueError("web_content surface cannot mark content human verified")
        if self.promote_to_evidence:
            raise ValueError("web_content surface cannot auto-promote content to evidence")
        if not self.requires_human_review:
            raise ValueError("web_content surface requires human review")
        return self


class WebContentSurfaceResult(BaseModel):
    """Result returned by the web_content surface."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "web.web_content"
    url: str = Field(min_length=1)
    title: str | None = None
    text_preview: str | None = None
    cache_key: str = Field(min_length=64, max_length=64)
    content_hash: str = Field(min_length=64, max_length=64)
    source_hygiene_status: str = Field(min_length=1)
    human_verified: bool = False
    promoted_to_evidence: bool = False
    requires_human_review: bool = True
    limitations: list[str] = Field(default_factory=list)

    @property
    def release_blocker(self) -> bool:
        """Return whether content was over-promoted."""

        return (
            self.human_verified
            or self.promoted_to_evidence
            or not self.requires_human_review
        )


def run_web_content_surface(request: WebContentSurfaceRequest) -> WebContentSurfaceResult:
    """Fetch in fake/default mode and convert to web content review context."""

    fetched = run_web_fetching_tool(WebFetchingToolRequest(url=request.url)).fetch_result
    content: WebContentToolResult = web_content_from_fetch_result(fetched)
    preview = content.text_content[:500] if content.text_content else None
    return WebContentSurfaceResult(
        url=content.url,
        title=content.title,
        text_preview=preview,
        cache_key=content.cache_key,
        content_hash=content.content_hash,
        source_hygiene_status=content.source_hygiene_status,
        human_verified=False,
        promoted_to_evidence=False,
        requires_human_review=content.requires_human_review,
        limitations=content.limitations,
    )
