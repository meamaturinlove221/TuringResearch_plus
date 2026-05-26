"""User-facing fake/default web_fetching tool wrapper."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, HttpUrl

from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import (
    RetrievalStatus,
    SourceType,
    WebFetchRequest,
    WebFetchResult,
)


class WebFetchingToolRequest(BaseModel):
    """Input for the public-safe web_fetching tool."""

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    source_type: SourceType = SourceType.PUBLIC_WEB
    fixture_path: Path | None = None
    dry_run: bool = True
    live_enabled: bool = False
    source_hygiene_status: str = "public_or_authorized"


class WebFetchingToolResult(BaseModel):
    """Output for the web_fetching tool."""

    model_config = ConfigDict(extra="forbid")

    fetch_result: WebFetchResult
    tool_name: str = "web_fetching"
    default_network: bool = False
    stores_cookies: bool = False
    requires_api_key: bool = False
    requires_human_review: bool = True

    @property
    def graceful_skip(self) -> bool:
        """Return whether the result is a safe no-key/no-live skip."""

        return self.fetch_result.retrieval_status in {
            RetrievalStatus.DRY_RUN,
            RetrievalStatus.LIVE_DISABLED,
            RetrievalStatus.SOURCE_BLOCKED,
        }


def run_web_fetching_tool(
    request: WebFetchingToolRequest,
    *,
    fetcher: WebFetcher | None = None,
) -> WebFetchingToolResult:
    """Run the fake/default web_fetching tool."""

    result = (fetcher or WebFetcher()).fetch(
        WebFetchRequest(
            url=request.url,
            source_type=request.source_type,
            fixture_path=request.fixture_path,
            dry_run=request.dry_run,
            live_enabled=request.live_enabled,
            source_hygiene_status=request.source_hygiene_status,
        )
    )
    return WebFetchingToolResult(fetch_result=result)


def render_web_fetching_usage(result: WebFetchingToolResult) -> str:
    """Render a compact web_fetching usage summary."""

    return "\n".join(
        [
            "# web_fetching",
            "",
            f"- URL: `{result.fetch_result.url}`",
            f"- Status: `{result.fetch_result.retrieval_status.value}`",
            f"- Default network: `{str(result.default_network).lower()}`",
            f"- Stores cookies: `{str(result.stores_cookies).lower()}`",
            f"- Requires API key: `{str(result.requires_api_key).lower()}`",
            f"- Requires human review: `{str(result.requires_human_review).lower()}`",
        ]
    ) + "\n"
