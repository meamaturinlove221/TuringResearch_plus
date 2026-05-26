"""Models for optional Advisor PPTX export."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AdvisorPptxBackend(StrEnum):
    """Supported optional PPTX writer backends."""

    PYTHON_PPTX = "python-pptx"


class AdvisorPptxExportStatus(StrEnum):
    """Outcome of an optional PPTX export attempt."""

    GENERATED = "generated"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


class AdvisorPptxSlide(BaseModel):
    """One review-safe slide in an advisor deck."""

    model_config = ConfigDict(extra="forbid")

    slide_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    bullets: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    not_ready: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def slide_requires_review_marker(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("Advisor PPTX slide requires human review")
        if self.not_ready and not any("not-ready" in item.lower() for item in self.bullets):
            raise ValueError("not-ready slide must include a not-ready marker")
        return self


class AdvisorRealPptxExportPlan(BaseModel):
    """Concrete optional PPTX export plan."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    output_filename: str = Field(default="advisor_deck.pptx", min_length=1)
    backend: AdvisorPptxBackend = AdvisorPptxBackend.PYTHON_PPTX
    deck_title: str = Field(min_length=1)
    slides: list[AdvisorPptxSlide]
    optional_backend: bool = True
    requires_human_review: bool = True
    safety_warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def pptx_plan_preserves_review_boundary(self) -> Self:
        if Path(self.output_filename).suffix.lower() != ".pptx":
            raise ValueError("PPTX export filename must end with .pptx")
        if not self.optional_backend:
            raise ValueError("PPTX export backend must remain optional")
        if not self.requires_human_review:
            raise ValueError("Advisor PPTX export requires human review")
        if len(self.slides) != 8:
            raise ValueError("Advisor PPTX export plan requires exactly 8 deck sections")
        return self


class AdvisorPptxExportResult(BaseModel):
    """Result of an optional PPTX export attempt."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    status: AdvisorPptxExportStatus
    backend: AdvisorPptxBackend = AdvisorPptxBackend.PYTHON_PPTX
    output_pptx: str | None = None
    skipped_reason: str | None = None
    generated_files: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def result_status_is_consistent(self) -> Self:
        if self.status == AdvisorPptxExportStatus.GENERATED:
            if not self.output_pptx:
                raise ValueError("generated PPTX result requires output_pptx")
            if self.skipped_reason:
                raise ValueError("generated PPTX result cannot include skipped_reason")
        if self.status == AdvisorPptxExportStatus.SKIPPED and not self.skipped_reason:
            raise ValueError("skipped PPTX result requires skipped_reason")
        if not self.requires_human_review:
            raise ValueError("Advisor PPTX export result requires human review")
        return self
