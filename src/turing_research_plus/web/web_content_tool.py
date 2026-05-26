"""web_content tool wrapper for already fetched or cached web content."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.web.html_extract import html_to_text
from turing_research_plus.web.models import WebContentCacheRecord, WebFetchResult


class WebContentToolResult(BaseModel):
    """Public-safe web_content output."""

    model_config = ConfigDict(extra="forbid")

    url: str = Field(min_length=1)
    title: str | None = None
    text_content: str | None = None
    content_hash: str = Field(min_length=64, max_length=64)
    cache_key: str = Field(min_length=64, max_length=64)
    source_hygiene_status: str
    human_verified: bool = False
    requires_human_review: bool = True
    limitations: list[str] = Field(default_factory=list)


def web_content_from_fetch_result(result: WebFetchResult) -> WebContentToolResult:
    """Create a web_content result from a fetch result."""

    text = result.text_content
    if text is None and result.html_content is not None:
        text = html_to_text(result.html_content)
    return WebContentToolResult(
        url=result.url,
        title=result.title,
        text_content=text,
        content_hash=result.content_hash,
        cache_key=result.cache_key,
        source_hygiene_status=result.source_metadata.source_hygiene_status,
        human_verified=False,
        requires_human_review=True,
        limitations=list(result.limitations)
        or ["web content is retrieved context, not verified evidence"],
    )


def web_content_from_cache_record(record: WebContentCacheRecord) -> WebContentToolResult:
    """Create a web_content result from an in-memory cache record."""

    return WebContentToolResult(
        url=record.url,
        title=None,
        text_content=record.text_content,
        content_hash=record.content_hash,
        cache_key=record.cache_key,
        source_hygiene_status=record.source_metadata.source_hygiene_status,
        human_verified=False,
        requires_human_review=True,
        limitations=["cached web content is not human verified"],
    )


def render_web_content_usage(result: WebContentToolResult) -> str:
    """Render a compact web_content usage summary."""

    return "\n".join(
        [
            "# web_content",
            "",
            f"- URL: `{result.url}`",
            f"- Source hygiene: `{result.source_hygiene_status}`",
            f"- Human verified: `{str(result.human_verified).lower()}`",
            f"- Requires human review: `{str(result.requires_human_review).lower()}`",
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in result.limitations],
        ]
    ) + "\n"
