"""Cached paper content tool surface."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.scholar_pipeline import (
    CachedPaperContent,
    read_cached_paper_content,
)


class PaperContentToolRequest(BaseModel):
    """Request for reading local cached paper Markdown."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    cached_markdown_path: Path
    live_enabled: bool = False
    automatic_full_paper_download: bool = False
    heavy_ocr_enabled: bool = False
    mineru_enabled: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_cached_content_boundary(self) -> Self:
        if self.live_enabled:
            raise ValueError("paper content tool reads cached local Markdown only")
        if self.automatic_full_paper_download:
            raise ValueError("paper content tool cannot download full papers")
        if self.heavy_ocr_enabled:
            raise ValueError("paper content tool does not run heavy OCR")
        if self.mineru_enabled:
            raise ValueError("paper content tool does not enable MinerU")
        if not self.requires_human_review:
            raise ValueError("paper content tool requires human review")
        return self


class PaperContentToolResult(BaseModel):
    """Result returned by the cached content tool."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "scholar.paper_content"
    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    markdown_path: str = Field(min_length=1)
    cache_hit: bool = True
    references_section_present: bool = False
    markdown_preview: str = Field(min_length=1)
    live_enabled: bool = False
    automatic_full_paper_download: bool = False
    heavy_ocr_enabled: bool = False
    mineru_enabled: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe content behavior was enabled."""

        return (
            self.live_enabled
            or self.automatic_full_paper_download
            or self.heavy_ocr_enabled
            or self.mineru_enabled
            or not self.requires_human_review
        )


def run_paper_content_tool(request: PaperContentToolRequest) -> PaperContentToolResult:
    """Read cached Markdown without downloading or OCR."""

    content: CachedPaperContent = read_cached_paper_content(
        paper_id=request.paper_id,
        title=request.title,
        markdown_path=request.cached_markdown_path,
    )
    preview = content.markdown[:500].strip() or "(empty cached Markdown)"
    return PaperContentToolResult(
        paper_id=content.paper_id,
        title=content.title,
        markdown_path=content.markdown_path,
        cache_hit=content.cache_hit,
        references_section_present=content.references_section() is not None,
        markdown_preview=preview,
        live_enabled=False,
        automatic_full_paper_download=False,
        heavy_ocr_enabled=False,
        mineru_enabled=False,
        requires_human_review=content.requires_human_review,
    )
