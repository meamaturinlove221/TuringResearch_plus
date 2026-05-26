"""Operator-facing fake/default web fetching surface."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator

from turing_research_plus.web import (
    WebFetchingToolRequest,
    WebFetchingToolResult,
    run_web_fetching_tool,
)


class WebFetchingSurfaceRequest(BaseModel):
    """Request for the v1.3 web_fetching surface."""

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    fixture_path: Path | None = None
    dry_run: bool = True
    live_enabled: bool = False
    source_hygiene_status: str = "public_or_authorized"
    stores_cookies: bool = False
    fetches_private_content: bool = False
    bypasses_paywall: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_fake_default_boundary(self) -> Self:
        if self.live_enabled and not self.dry_run:
            raise ValueError("web_fetching surface cannot enable live mode by default")
        if self.stores_cookies:
            raise ValueError("web_fetching surface cannot store cookies")
        if self.fetches_private_content:
            raise ValueError("web_fetching surface cannot fetch private content")
        if self.bypasses_paywall:
            raise ValueError("web_fetching surface cannot bypass paywalls")
        if not self.requires_human_review:
            raise ValueError("web_fetching surface requires human review")
        return self


class WebFetchingSurfaceResult(BaseModel):
    """Result returned by the web_fetching surface."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "web.web_fetching"
    url: str = Field(min_length=1)
    retrieval_status: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    title: str | None = None
    cache_key: str = Field(min_length=64, max_length=64)
    content_hash: str = Field(min_length=64, max_length=64)
    warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    default_network: bool = False
    live_enabled: bool = False
    stores_cookies: bool = False
    requires_api_key: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe fetch behavior was enabled."""

        return (
            self.default_network
            or self.live_enabled
            or self.stores_cookies
            or self.requires_api_key
            or not self.requires_human_review
        )


def run_web_fetching_surface(
    request: WebFetchingSurfaceRequest,
) -> WebFetchingSurfaceResult:
    """Run the fake/default web_fetching surface."""

    result: WebFetchingToolResult = run_web_fetching_tool(
        WebFetchingToolRequest(
            url=request.url,
            fixture_path=request.fixture_path,
            dry_run=request.dry_run,
            live_enabled=request.live_enabled,
            source_hygiene_status=request.source_hygiene_status,
        )
    )
    fetched = result.fetch_result
    return WebFetchingSurfaceResult(
        url=fetched.url,
        retrieval_status=fetched.retrieval_status.value,
        source_type=fetched.source_type.value,
        title=fetched.title,
        cache_key=fetched.cache_key,
        content_hash=fetched.content_hash,
        warnings=fetched.warnings,
        limitations=fetched.limitations,
        default_network=False,
        live_enabled=False,
        stores_cookies=False,
        requires_api_key=False,
        requires_human_review=fetched.requires_human_review,
    )
