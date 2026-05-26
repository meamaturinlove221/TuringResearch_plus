"""Models for public case study drafts."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CaseStudyStatus(StrEnum):
    """Public case study readiness labels."""

    DRAFT = "draft"
    REVIEW_REQUIRED = "requires-human-review"
    BLOCKED = "blocked"


class CaseStudySection(BaseModel):
    """One public case study section."""

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    bullets: list[str] = Field(default_factory=list)
    status: CaseStudyStatus = CaseStudyStatus.REVIEW_REQUIRED
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class CaseStudyRedaction(BaseModel):
    """One redaction applied or proposed for public case study output."""

    model_config = ConfigDict(extra="forbid")

    finding_type: str = Field(min_length=1)
    original_hint: str = Field(min_length=1)
    replacement: str = Field(min_length=1)
    applied: bool = True
    release_blocker: bool = False
    requires_human_review: bool = True


class CaseStudyRedactionReport(BaseModel):
    """Redaction report for public case study material."""

    model_config = ConfigDict(extra="forbid")

    redactions: list[CaseStudyRedaction] = Field(default_factory=list)
    sanitized: bool = True
    release_blockers: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class CaseStudyClaimFinding(BaseModel):
    """One unsupported or unsafe public-claim finding."""

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    replacement: str = Field(min_length=1)
    severity: str = Field(default="blocker", min_length=1)
    requires_human_review: bool = True


class CaseStudyClaimSafetyReport(BaseModel):
    """Claim safety report for case study draft."""

    model_config = ConfigDict(extra="forbid")

    findings: list[CaseStudyClaimFinding] = Field(default_factory=list)
    unsupported_experiment_claims: list[str] = Field(default_factory=list)
    safe_to_publish: bool = False
    requires_human_review: bool = True


class CaseStudyDraft(BaseModel):
    """A sanitized public case study draft."""

    model_config = ConfigDict(extra="forbid")

    case_study_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    problem_background: CaseStudySection
    why_turingresearch_was_useful: CaseStudySection
    route_changes: CaseStudySection
    evidence_management: CaseStudySection
    failures_and_blockers: CaseStudySection
    advisor_pack: CaseStudySection
    what_remains_human_work: CaseStudySection
    what_not_to_claim: CaseStudySection
    redaction_report: CaseStudyRedactionReport
    claim_safety_report: CaseStudyClaimSafetyReport
    status: CaseStudyStatus = CaseStudyStatus.REVIEW_REQUIRED
    public_demo_only: bool = True
    published: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def draft_stays_public_review_only(self) -> Self:
        if self.published:
            raise ValueError("case study builder must not publish")
        if not self.public_demo_only:
            raise ValueError("case study draft must be public-demo only")
        if not self.requires_human_review:
            raise ValueError("case study draft requires human review")
        return self

    @property
    def sections(self) -> list[CaseStudySection]:
        """Return sections in report order."""

        return [
            self.problem_background,
            self.why_turingresearch_was_useful,
            self.route_changes,
            self.evidence_management,
            self.failures_and_blockers,
            self.advisor_pack,
            self.what_remains_human_work,
            self.what_not_to_claim,
        ]
