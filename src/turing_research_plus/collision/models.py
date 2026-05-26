"""Models for Paper Collision Risk Detector."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CollisionRiskLevel(StrEnum):
    """Stable risk levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    UNKNOWN = "unknown"


class OverlapDimension(StrEnum):
    """Dimensions used for paper collision overlap."""

    TASK = "task"
    INPUT = "input"
    OUTPUT = "output"
    REPRESENTATION = "representation"
    MODEL_COMPONENT = "model component"
    HUMAN_PRIOR_USAGE = "human prior usage"
    SMPL_SMPLX_ENCODING = "SMPL / SMPL-X encoding"
    VGGT_TOKEN_INTEGRATION = "VGGT token integration"
    EVALUATION_TARGET = "evaluation target"
    DATASET = "dataset"
    CLAIMED_CONTRIBUTION = "claimed contribution"


class OverlapScore(BaseModel):
    """One overlap dimension score."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    dimension: OverlapDimension
    score: float = Field(ge=0, le=1)
    rationale: str = Field(min_length=1)
    requires_real_paper_review: bool = True


class OverlapMatrix(BaseModel):
    """Overlap scores grouped by compared papers."""

    model_config = ConfigDict(extra="forbid")

    rows: list[OverlapScore] = Field(default_factory=list)

    def for_paper(self, paper_id: str) -> list[OverlapScore]:
        return [row for row in self.rows if row.paper_id == paper_id]


class RiskScore(BaseModel):
    """Aggregate collision risk for one compared paper."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    level: CollisionRiskLevel
    score: float = Field(ge=0, le=1)
    rationale: str = Field(min_length=1)
    requires_human_review: bool = True


class SafeClaim(BaseModel):
    """A conservative claim that can be made from current evidence."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    basis: str = Field(min_length=1)
    caveat: str = Field(min_length=1)


class UnsafeClaim(BaseModel):
    """A claim that should not be made yet."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class PaperComparisonInput(BaseModel):
    """Input to the collision detector."""

    model_config = ConfigDict(extra="forbid")

    target_project: str = Field(default="VGGT/SMPL-X feature adapter", min_length=1)
    compared_papers: list[dict[str, object]] = Field(default_factory=list)
    citation_graph: dict[str, object] | None = None
    source_status: str = "fake-or-manual-note"


class CollisionRiskReport(BaseModel):
    """Collision risk report for VGGT paper positioning."""

    model_config = ConfigDict(extra="forbid")

    target_project: str = Field(min_length=1)
    compared_papers: list[dict[str, object]] = Field(default_factory=list)
    overlap_matrix: OverlapMatrix
    risk_scores: list[RiskScore] = Field(default_factory=list)
    safe_claims: list[SafeClaim] = Field(default_factory=list)
    unsafe_claims: list[UnsafeClaim] = Field(default_factory=list)
    positioning_notes: list[str] = Field(default_factory=list)
    missing_evidence: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def no_definitive_no_collision_without_evidence(self) -> CollisionRiskReport:
        for claim in self.safe_claims:
            if "definitive no collision" in claim.text.lower():
                raise ValueError("definitive no collision is not allowed without real evidence")
        return self
