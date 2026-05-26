"""Models for paper deep review mode."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DeepReviewStatus(StrEnum):
    """Reading/review status labels."""

    NOT_STARTED = "not-started"
    SCAFFOLD_ONLY = "scaffold-only"
    NEEDS_REAL_PAPER = "needs-real-paper"
    IN_REVIEW = "in-review"
    REVIEW_READY = "review-ready"
    BLOCKED = "blocked"


class DeepReviewItemKind(StrEnum):
    """Checklist item categories."""

    FIGURE = "figure"
    EQUATION = "equation"
    TABLE = "table"
    IMPLEMENTATION = "implementation"
    REPRODUCTION = "reproduction"
    CLAIM = "claim"
    ADVISOR_NOTE = "advisor-note"


class DeepReviewItem(BaseModel):
    """One paper deep-review checklist item."""

    model_config = ConfigDict(extra="forbid")

    item_id: str = Field(min_length=1)
    kind: DeepReviewItemKind
    description: str = Field(min_length=1)
    source_status: str = Field(default="requires-real-paper-review", min_length=1)
    status: DeepReviewStatus = DeepReviewStatus.NEEDS_REAL_PAPER
    requires_human_review: bool = True

    @model_validator(mode="after")
    def item_requires_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("deep review checklist items require human review")
        return self


class DeepReviewReport(BaseModel):
    """Deep review report for a paper candidate."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_status: str = Field(min_length=1)
    reading_status: DeepReviewStatus
    figures_to_inspect: list[DeepReviewItem] = Field(default_factory=list)
    equations_to_inspect: list[DeepReviewItem] = Field(default_factory=list)
    tables_to_inspect: list[DeepReviewItem] = Field(default_factory=list)
    implementation_questions: list[DeepReviewItem] = Field(default_factory=list)
    reproduction_blockers: list[DeepReviewItem] = Field(default_factory=list)
    relation_to_our_project: list[str] = Field(default_factory=list)
    claims_requiring_verification: list[DeepReviewItem] = Field(default_factory=list)
    notes_for_advisor: list[DeepReviewItem] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    copied_long_text: bool = False
    fabricated_equations: bool = False
    downloaded_pdf: bool = False
    generated_final_conclusion: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def report_stays_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("deep review report requires human review")
        if self.copied_long_text:
            raise ValueError("deep review report must not copy long paper text")
        if self.fabricated_equations:
            raise ValueError("deep review report must not fabricate equations")
        if self.downloaded_pdf:
            raise ValueError("deep review report must not download PDFs")
        if self.generated_final_conclusion:
            raise ValueError("deep review report must not generate final conclusions")
        if not self.figures_to_inspect:
            raise ValueError("deep review report must list figures to inspect")
        if not self.equations_to_inspect:
            raise ValueError("deep review report must list equations to inspect")
        if not self.tables_to_inspect:
            raise ValueError("deep review report must list tables to inspect")
        if not self.reproduction_blockers:
            raise ValueError("deep review report must list reproduction blockers")
        return self
