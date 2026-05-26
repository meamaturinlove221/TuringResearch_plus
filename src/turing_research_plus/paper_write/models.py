"""Models for safe paper writing scaffolds."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PaperSectionStatus(StrEnum):
    """Allowed section readiness labels."""

    OUTLINE_ONLY = "outline-only"
    NEEDS_EVIDENCE = "needs-evidence"
    NEEDS_HUMAN_REVIEW = "needs-human-review"
    BLOCKED_UNSAFE_CLAIMS = "blocked-unsafe-claims"
    READY_FOR_DRAFTING = "ready-for-drafting"


class EvidenceRequirement(BaseModel):
    """One evidence requirement for a paper section."""

    model_config = ConfigDict(extra="forbid")

    requirement_id: str = Field(min_length=1)
    section: str = Field(min_length=1)
    description: str = Field(min_length=1)
    status: str = Field(min_length=1)
    source_refs: list[str] = Field(default_factory=list)
    required_before_claim: bool = True


class PaperSectionPlan(BaseModel):
    """Plan-only outline for one paper section."""

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: PaperSectionStatus
    bullets: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    unsafe_claims: list[str] = Field(default_factory=list)
    human_review_notes: list[str] = Field(default_factory=list)


class PaperScaffold(BaseModel):
    """Paper writing scaffold that never claims final paper conclusions."""

    model_config = ConfigDict(extra="forbid")

    scaffold_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    title_candidates: list[str] = Field(default_factory=list)
    abstract_status: PaperSectionStatus
    introduction_plan: PaperSectionPlan
    related_work_plan: PaperSectionPlan
    method_plan: PaperSectionPlan
    experiment_plan: PaperSectionPlan
    results_status: PaperSectionStatus
    limitation_plan: PaperSectionPlan
    evidence_requirements: list[EvidenceRequirement] = Field(default_factory=list)
    missing_experiments: list[str] = Field(default_factory=list)
    unsafe_claims: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    generated_final_abstract: bool = False
    generated_final_results: bool = False

    @model_validator(mode="after")
    def scaffold_never_claims_final_paper_text(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("paper scaffold requires human review")
        if self.generated_final_abstract:
            raise ValueError("paper scaffold must not generate final abstract")
        if self.generated_final_results:
            raise ValueError("paper scaffold must not generate final results")
        if self.results_status == PaperSectionStatus.READY_FOR_DRAFTING:
            raise ValueError("results cannot be ready without real experiment evidence")
        if not self.evidence_requirements:
            raise ValueError("paper scaffold must list evidence requirements")
        if not self.missing_experiments:
            raise ValueError("paper scaffold must list missing experiments")
        return self
