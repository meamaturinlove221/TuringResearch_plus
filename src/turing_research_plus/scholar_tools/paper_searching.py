"""Fake/default paper searching tool surface."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.scholar_pipeline import (
    ScholarPipelineRequest,
    ScholarPipelineResult,
    run_scholar_search_pipeline,
)


class PaperSearchingToolRequest(BaseModel):
    """Request for the public Scholar paper searching tool."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    paper_id: str | None = None
    cached_markdown_path: Path | None = None
    known_arxiv_url: str | None = None
    manual_fallback: list[dict[str, Any]] = Field(default_factory=list)
    live_enabled: bool = False
    dry_run: bool = True
    automatic_full_paper_download: bool = False
    mineru_enabled: bool = False
    paywall_bypass_allowed: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_fake_default_boundary(self) -> Self:
        if self.live_enabled and not self.dry_run:
            raise ValueError("paper searching tool cannot enable live mode by default")
        if self.automatic_full_paper_download:
            raise ValueError("paper searching tool cannot download full papers automatically")
        if self.mineru_enabled:
            raise ValueError("paper searching tool does not enable MinerU")
        if self.paywall_bypass_allowed:
            raise ValueError("paper searching tool cannot bypass paywalls")
        if not self.requires_human_review:
            raise ValueError("paper searching tool requires human review")
        return self


class PaperSearchingToolResult(BaseModel):
    """Result returned by the paper searching tool surface."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "scholar.paper_searching"
    query: str = Field(min_length=1)
    selected_source: str = Field(min_length=1)
    status: str = Field(min_length=1)
    papers: list[dict[str, Any]] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    live_enabled: bool = False
    no_real_api_key_required: bool = True
    automatic_full_paper_download: bool = False
    mineru_enabled: bool = False
    paywall_bypass_allowed: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe search behavior was enabled."""

        return (
            self.live_enabled
            or self.automatic_full_paper_download
            or self.mineru_enabled
            or self.paywall_bypass_allowed
            or not self.requires_human_review
        )


def run_paper_searching_tool(request: PaperSearchingToolRequest) -> PaperSearchingToolResult:
    """Run cache-first fake/default paper search."""

    result: ScholarPipelineResult = run_scholar_search_pipeline(
        ScholarPipelineRequest(
            query=request.query,
            paper_id=request.paper_id,
            cached_markdown_path=request.cached_markdown_path,
            known_arxiv_url=request.known_arxiv_url,
            manual_fallback=request.manual_fallback,
            live_enabled=request.live_enabled,
            dry_run=request.dry_run,
        )
    )
    return PaperSearchingToolResult(
        query=result.query,
        selected_source=result.selected_source.value,
        status=result.status.value,
        papers=result.papers,
        limitations=result.limitations,
        live_enabled=False,
        no_real_api_key_required=True,
        automatic_full_paper_download=False,
        mineru_enabled=False,
        paywall_bypass_allowed=False,
        requires_human_review=result.requires_human_review,
    )
