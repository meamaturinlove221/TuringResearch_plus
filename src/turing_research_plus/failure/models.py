"""Models for failure taxonomy and attribution."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef


class FailureCategory(StrEnum):
    """Canonical VGGT / long-route failure categories."""

    FAST_RETURN = "FAST_RETURN"
    REPORT_ONLY = "REPORT_ONLY"
    IDENTITY_COPY = "IDENTITY_COPY"
    FALLBACK_ONLY = "FALLBACK_ONLY"
    REAL_BACKEND_UNAVAILABLE = "REAL_BACKEND_UNAVAILABLE"
    MISSING_ASSETS = "MISSING_ASSETS"
    VISUAL_PROOF_INSUFFICIENT = "VISUAL_PROOF_INSUFFICIENT"
    FULL_BODY_REGRESSION = "FULL_BODY_REGRESSION"
    HAIRLINE_REGRESSION = "HAIRLINE_REGRESSION"
    HAND_OBJECT_CONFUSION = "HAND_OBJECT_CONFUSION"
    DEPTH_POINT_SCHEMA_MISMATCH = "DEPTH_POINT_SCHEMA_MISMATCH"
    PACKAGE_INCOMPLETE = "PACKAGE_INCOMPLETE"
    SPARSE_BACKEND_UNAVAILABLE = "SPARSE_BACKEND_UNAVAILABLE"
    SMPLX_ALIGNMENT_WEAK = "SMPLX_ALIGNMENT_WEAK"
    NOT_ENOUGH_EVIDENCE = "NOT_ENOUGH_EVIDENCE"
    PROMOTION_FORBIDDEN = "PROMOTION_FORBIDDEN"
    STRICT_REGISTRY_FORBIDDEN = "STRICT_REGISTRY_FORBIDDEN"
    HUMAN_REVIEW_REQUIRED = "HUMAN_REVIEW_REQUIRED"


class FailureSeverity(StrEnum):
    """Failure severity."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class RetryPolicy(StrEnum):
    """Retry policy labels."""

    DO_NOT_RETRY = "do-not-retry"
    RETRY_AFTER_FIX = "retry-after-fix"
    REQUIRES_REAL_EXPERIMENT = "requires-real-experiment"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"


class FailureTaxonomyEntry(BaseModel):
    """One taxonomy entry."""

    model_config = ConfigDict(extra="forbid")

    category: FailureCategory
    severity: FailureSeverity
    description: str = Field(min_length=1)
    default_retry_policy: RetryPolicy
    default_next_actions: list[str] = Field(min_length=1)


class FailureInstance(BaseModel):
    """Raw or normalized failure input."""

    model_config = ConfigDict(extra="forbid")

    failure_id: str = Field(min_length=1)
    related_route_id: str | None = None
    related_stage_id: str | None = None
    related_run_id: str | None = None
    text: str = Field(min_length=1)
    category_hint: FailureCategory | None = None
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class FailureAnalysisInput(BaseModel):
    """Input for failure analysis."""

    model_config = ConfigDict(extra="forbid")

    failures: list[FailureInstance] = Field(min_length=1)


class FailureAttributionReport(BaseModel):
    """Attribution report for one canonical failure."""

    model_config = ConfigDict(extra="forbid")

    failure_id: str = Field(min_length=1)
    related_route_id: str | None = None
    related_stage_id: str | None = None
    related_run_id: str | None = None
    category: FailureCategory
    severity: FailureSeverity
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    likely_causes: list[str] = Field(min_length=1)
    ruled_out_causes: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(min_length=1)
    retry_policy: RetryPolicy
    requires_human_review: bool = False

    @model_validator(mode="after")
    def evidence_or_review_required(self) -> Self:
        if not self.evidence_refs and not self.requires_human_review:
            raise ValueError("failure attribution requires evidence_refs or requires_human_review")
        return self

    def to_markdown(self) -> str:
        """Render a compact Markdown report."""

        lines = [
            f"# Failure Attribution: {self.failure_id}",
            "",
            f"- Category: {self.category.value}",
            f"- Severity: {self.severity.value}",
            f"- Retry policy: {self.retry_policy.value}",
            f"- Requires human review: {str(self.requires_human_review).lower()}",
            "",
            "## Likely Causes",
            "",
            *[f"- {item}" for item in self.likely_causes],
            "",
            "## Ruled Out Causes",
            "",
            *[f"- {item}" for item in self.ruled_out_causes],
            "",
            "## Next Actions",
            "",
            *[f"- {item}" for item in self.next_actions],
        ]
        return "\n".join(lines) + "\n"
