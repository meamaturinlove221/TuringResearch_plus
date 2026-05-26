"""Models for the refined scholar pipeline."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.adapters.models import SourceMetadata


class ScholarSourcePriority(StrEnum):
    """Source priority for paper discovery."""

    CACHED_MARKDOWN = "cached_markdown"
    ARXIV = "arxiv"
    SEMANTIC_SCHOLAR = "semantic_scholar"
    UNPAYWALL_PLACEHOLDER = "unpaywall_placeholder"
    MANUAL = "manual"


class ScholarPipelineStatus(StrEnum):
    """Scholar pipeline status."""

    CACHE_HIT = "cache_hit"
    FAKE_RESULT = "fake_result"
    MANUAL_FALLBACK = "manual_fallback"
    LIVE_OPTIONAL_DISABLED = "live_optional_disabled"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"


class ReferenceSource(StrEnum):
    """Reference source fallback order."""

    SEMANTIC_SCHOLAR = "semantic_scholar"
    CACHED_MARKDOWN = "cached_markdown"
    MANUAL = "manual"
    UNKNOWN = "unknown"


class PaperReference(BaseModel):
    """One extracted or provider-supplied reference."""

    model_config = ConfigDict(extra="forbid")

    reference_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source: ReferenceSource
    source_metadata: list[SourceMetadata] = Field(default_factory=list)
    requires_human_review: bool = True


class CachedPaperContent(BaseModel):
    """Cached local Markdown paper content."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    markdown_path: str = Field(min_length=1)
    markdown: str = Field(min_length=1)
    cache_hit: bool = True
    source_metadata: list[SourceMetadata] = Field(default_factory=list)
    requires_human_review: bool = True

    def references_section(self) -> str | None:
        """Return a cached references section when present."""

        markers = ["## References", "# References", "References\n"]
        for marker in markers:
            index = self.markdown.find(marker)
            if index >= 0:
                return self.markdown[index:]
        return None


class ScholarPipelineRequest(BaseModel):
    """Input for cache-first scholar lookup."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    paper_id: str | None = None
    cached_markdown_path: Path | None = None
    known_arxiv_url: str | None = None
    manual_fallback: list[dict[str, Any]] = Field(default_factory=list)
    live_enabled: bool = False
    dry_run: bool = True


class ScholarPipelineResult(BaseModel):
    """Output for cache-first scholar lookup."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    source_priority: list[ScholarSourcePriority]
    selected_source: ScholarSourcePriority
    status: ScholarPipelineStatus
    papers: list[dict[str, Any]] = Field(default_factory=list)
    cached_content: CachedPaperContent | None = None
    source_metadata: list[SourceMetadata] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def live_results_are_not_verified(self) -> Self:
        for source in self.source_metadata:
            if source.human_verified:
                raise ValueError("scholar pipeline cannot mark sources as human verified")
        return self

    def to_markdown(self) -> str:
        """Render a Markdown search summary."""

        lines = [
            f"# Scholar Pipeline Result: {self.query}",
            "",
            f"- Selected source: `{self.selected_source.value}`",
            f"- Status: `{self.status.value}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "",
            "## Papers",
            "",
        ]
        lines.extend(
            [
                f"- {paper.get('title', 'untitled')} "
                f"(`{paper.get('paper_id') or paper.get('arxiv_id') or 'manual'}`)"
                for paper in self.papers
            ]
            or ["- none"]
        )
        lines.extend(["", "## Limitations", ""])
        lines.extend([f"- {item}" for item in self.limitations] or ["- none recorded"])
        return "\n".join(lines) + "\n"


class ReferencePipelineRequest(BaseModel):
    """Input for reference resolution."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str | None = None
    cached_markdown: str | None = None
    manual_references: list[str] = Field(default_factory=list)
    live_enabled: bool = False
    dry_run: bool = True
    limit: int = Field(default=20, ge=1, le=100)


class ReferencePipelineResult(BaseModel):
    """Output for reference resolution with fallback source."""

    model_config = ConfigDict(extra="forbid")

    source: ReferenceSource
    references: list[PaperReference] = Field(default_factory=list)
    pagination_used: bool = False
    fallback_used: bool = False
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    def to_markdown(self) -> str:
        """Render references as Markdown."""

        lines = [
            "# Reference Pipeline Result",
            "",
            f"- Source: `{self.source.value}`",
            f"- Fallback used: `{str(self.fallback_used).lower()}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            "",
            "## References",
            "",
        ]
        lines.extend(
            [f"- {ref.title} (`{ref.source.value}`)" for ref in self.references]
            or ["- none"]
        )
        return "\n".join(lines) + "\n"


class ThreePassReadingPlan(BaseModel):
    """Keshav-style three-pass reading plan."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    pass_1: list[str] = Field(min_length=1)
    pass_2: list[str] = Field(min_length=1)
    pass_3: list[str] = Field(min_length=1)
    outputs: list[str] = Field(
        default_factory=lambda: [
            "method card",
            "collision notes",
            "borrow/not-copy list",
            "VGGT mapping",
        ]
    )
    requires_real_paper_review: bool = True
    human_verified: bool = False

    @model_validator(mode="after")
    def fake_plan_is_not_human_verified(self) -> Self:
        if self.human_verified:
            raise ValueError("three-pass template cannot be marked human verified")
        return self

    def to_markdown(self) -> str:
        """Render the reading plan as Markdown."""

        lines = [
            f"# Three-Pass Reading Plan: {self.title}",
            "",
            f"- Paper ID: `{self.paper_id}`",
            f"- Requires real paper review: `{str(self.requires_real_paper_review).lower()}`",
            "",
            "## Pass 1: Bird's-Eye Scan",
            "",
            *[f"- {item}" for item in self.pass_1],
            "",
            "## Pass 2: Content Grasp",
            "",
            *[f"- {item}" for item in self.pass_2],
            "",
            "## Pass 3: Deep Understanding",
            "",
            *[f"- {item}" for item in self.pass_3],
            "",
            "## Outputs",
            "",
            *[f"- {item}" for item in self.outputs],
        ]
        return "\n".join(lines) + "\n"
