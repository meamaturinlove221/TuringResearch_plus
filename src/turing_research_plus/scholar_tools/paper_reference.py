"""Paper reference resolution tool surface."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.scholar_pipeline import (
    ReferencePipelineRequest,
    ReferencePipelineResult,
    resolve_references,
)


class PaperReferenceToolRequest(BaseModel):
    """Request for reference resolution."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str | None = None
    cached_markdown: str | None = None
    manual_references: list[str] = Field(default_factory=list)
    live_enabled: bool = False
    dry_run: bool = True
    limit: int = Field(default=20, ge=1, le=100)


class PaperReferenceToolResult(BaseModel):
    """Result returned by the reference tool surface."""

    model_config = ConfigDict(extra="forbid")

    tool_name: str = "scholar.paper_reference"
    source: str = Field(min_length=1)
    references: list[dict[str, str]] = Field(default_factory=list)
    pagination_used: bool = False
    fallback_used: bool = False
    limitations: list[str] = Field(default_factory=list)
    live_enabled: bool = False
    paywall_bypass_allowed: bool = False
    automatic_full_paper_download: bool = False
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether unsafe reference behavior was enabled."""

        return (
            self.live_enabled
            or self.paywall_bypass_allowed
            or self.automatic_full_paper_download
            or not self.requires_human_review
        )


def run_paper_reference_tool(request: PaperReferenceToolRequest) -> PaperReferenceToolResult:
    """Resolve references through fake/default or cached/manual fallback."""

    result: ReferencePipelineResult = resolve_references(
        ReferencePipelineRequest(
            paper_id=request.paper_id,
            cached_markdown=request.cached_markdown,
            manual_references=request.manual_references,
            live_enabled=request.live_enabled,
            dry_run=request.dry_run,
            limit=request.limit,
        )
    )
    return PaperReferenceToolResult(
        source=result.source.value,
        references=[
            {
                "reference_id": reference.reference_id,
                "title": reference.title,
                "source": reference.source.value,
            }
            for reference in result.references
        ],
        pagination_used=result.pagination_used,
        fallback_used=result.fallback_used,
        limitations=result.limitations,
        live_enabled=False,
        paywall_bypass_allowed=False,
        automatic_full_paper_download=False,
        requires_human_review=result.requires_human_review,
    )
