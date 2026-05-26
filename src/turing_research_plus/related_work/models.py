"""Models for conservative related-work positioning."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PaperGroup(StrEnum):
    """Supported related-work groups."""

    FEED_FORWARD_GEOMETRY = "feed_forward_geometry"
    HUMAN_PRIOR_MODELS = "human_prior_models"
    SMPL_SMPLX_ENCODING = "smpl_smplx_encoding"
    NEURALBODY_SPARSE_VOXEL = "neuralbody_sparse_voxel"
    HUMANRAM_TRIPLANE_RASTER = "humanram_triplane_raster"
    VGGT_HUMAN_EXTENSIONS = "vggt_human_extensions"
    SPARSECONV_BACKENDS = "sparseconv_backends"
    RECONSTRUCTION_OR_ANIMATION = "reconstruction_or_animation"
    UNKNOWN_OR_REQUIRES_REVIEW = "unknown_or_requires_review"


class PositioningClaim(BaseModel):
    """A safe or unsafe related-work claim."""

    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1)
    basis: str = Field(min_length=1)
    caveat: str = Field(min_length=1)
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class MissingEvidenceItem(BaseModel):
    """A missing evidence item for related-work positioning."""

    model_config = ConfigDict(extra="forbid")

    item: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    required_action: str = Field(min_length=1)


class PaperGroupEntry(BaseModel):
    """Paper assigned to a related-work group."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    group: PaperGroup
    rationale: str = Field(min_length=1)
    requires_real_paper_review: bool = True


class MethodCluster(BaseModel):
    """Cluster of methods used to plan related-work sections."""

    model_config = ConfigDict(extra="forbid")

    cluster_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    papers: list[str] = Field(default_factory=list)
    positioning_note: str = Field(min_length=1)
    requires_human_review: bool = True


class RelatedWorkPositioningInput(BaseModel):
    """Input for building a related-work positioning report."""

    model_config = ConfigDict(extra="forbid")

    project_topic: str = Field(default="VGGT / SMPL-X feature encoding", min_length=1)
    method_cards: list[dict[str, object]] = Field(default_factory=list)
    citation_graph: dict[str, object] | None = None
    collision_report: dict[str, object] | None = None
    web_summaries: list[dict[str, object]] = Field(default_factory=list)
    manual_notes: list[str] = Field(default_factory=list)


class RelatedWorkPositioningReport(BaseModel):
    """Conservative report for related-work planning."""

    model_config = ConfigDict(extra="forbid")

    project_topic: str = Field(min_length=1)
    paper_groups: list[PaperGroupEntry] = Field(default_factory=list)
    method_clusters: list[MethodCluster] = Field(default_factory=list)
    overlap_summary: list[str] = Field(default_factory=list)
    differentiation_points: list[str] = Field(default_factory=list)
    safe_claims: list[PositioningClaim] = Field(default_factory=list)
    unsafe_claims: list[PositioningClaim] = Field(default_factory=list)
    missing_evidence: list[MissingEvidenceItem] = Field(default_factory=list)
    recommended_related_work_structure: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def no_definitive_claims(self) -> RelatedWorkPositioningReport:
        for claim in self.safe_claims:
            lowered = claim.text.lower()
            if "definitive" in lowered or "complete review" in lowered:
                raise ValueError("safe claims cannot be definitive or claim complete review")
        return self
