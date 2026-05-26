"""Models for optional Advisor PDF export."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class AdvisorPdfBackend(StrEnum):
    """Supported optional PDF writer backends."""

    REPORTLAB = "reportlab"


class AdvisorPdfExportStatus(StrEnum):
    """Outcome of an optional PDF export attempt."""

    GENERATED = "generated"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


class AdvisorRealPdfExportPlan(BaseModel):
    """Concrete PDF export plan from an Advisor Markdown Bundle."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    output_filename: str = Field(default="advisor_report.pdf", min_length=1)
    backend: AdvisorPdfBackend = AdvisorPdfBackend.REPORTLAB
    title: str = Field(min_length=1)
    sections: list[str] = Field(default_factory=list)
    source_files: list[str] = Field(default_factory=list)
    optional_backend: bool = True
    requires_human_review: bool = True
    safety_warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def pdf_plan_preserves_review_boundary(self) -> Self:
        if Path(self.output_filename).suffix.lower() != ".pdf":
            raise ValueError("PDF export filename must end with .pdf")
        if not self.optional_backend:
            raise ValueError("PDF export backend must remain optional")
        if not self.requires_human_review:
            raise ValueError("Advisor PDF export requires human review")
        required_sections = {
            "title",
            "current status",
            "evidence summary",
            "artifact readiness",
            "visual readiness",
            "failure summary",
            "next actions",
            "limitations",
            "requires human review",
        }
        present = {section.strip().lower() for section in self.sections}
        missing = required_sections - present
        if missing:
            raise ValueError(f"PDF export plan missing sections: {sorted(missing)}")
        return self


class AdvisorPdfExportResult(BaseModel):
    """Result of an optional PDF export attempt."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    source_bundle_id: str = Field(min_length=1)
    status: AdvisorPdfExportStatus
    backend: AdvisorPdfBackend = AdvisorPdfBackend.REPORTLAB
    output_pdf: str | None = None
    skipped_reason: str | None = None
    generated_files: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def result_status_is_consistent(self) -> Self:
        if self.status == AdvisorPdfExportStatus.GENERATED:
            if not self.output_pdf:
                raise ValueError("generated PDF result requires output_pdf")
            if self.skipped_reason:
                raise ValueError("generated PDF result cannot include skipped_reason")
        if self.status == AdvisorPdfExportStatus.SKIPPED and not self.skipped_reason:
            raise ValueError("skipped PDF result requires skipped_reason")
        if not self.requires_human_review:
            raise ValueError("Advisor PDF export result requires human review")
        return self
