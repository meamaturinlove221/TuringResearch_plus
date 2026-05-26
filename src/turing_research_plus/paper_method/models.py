"""Models for Paper-to-Method Card."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef


class PaperSourceType(StrEnum):
    """Supported paper method source types."""

    PDF_MARKDOWN = "pdf_markdown"
    HTML_SUMMARY = "html_summary"
    MANUAL_NOTE = "manual_note"
    FAKE_OR_MANUAL_NOTE = "fake-or-manual-note"


class CollisionRisk(StrEnum):
    """Collision risk against VGGT objectives."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    REQUIRES_REVIEW = "requires-review"


class VGGTMethodMapping(BaseModel):
    """How a paper method relates to VGGT dogfooding."""

    model_config = ConfigDict(extra="forbid")

    smpl_role: str = Field(min_length=1)
    voxel_sparseconv_relevance: str = Field(min_length=1)
    triplane_relevance: str = Field(min_length=1)
    token_alignment_relevance: str = Field(min_length=1)
    geometry_output_relevance: str = Field(min_length=1)
    difference_from_vggt_objective: str = Field(min_length=1)
    potential_collision_risk: CollisionRisk


class PaperMethodCard(BaseModel):
    """Structured method card for a paper or paper-like note."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_type: PaperSourceType
    task: str = Field(min_length=1)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    representation: list[str] = Field(default_factory=list)
    core_method: str = Field(min_length=1)
    architecture_components: list[str] = Field(default_factory=list)
    training_objective: str = Field(min_length=1)
    inference_pipeline: list[str] = Field(default_factory=list)
    key_figures: list[str] = Field(default_factory=list)
    key_tables: list[str] = Field(default_factory=list)
    what_to_borrow: list[str] = Field(default_factory=list)
    what_not_to_copy: list[str] = Field(default_factory=list)
    collision_risk: CollisionRisk
    mapping_to_vggt: VGGTMethodMapping
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def evidence_or_review_required(self) -> Self:
        if not self.evidence_refs and not self.requires_human_review:
            raise ValueError("method card without evidence_refs requires human review")
        if (
            self.source_type == PaperSourceType.FAKE_OR_MANUAL_NOTE
            and not self.requires_human_review
        ):
            raise ValueError("fake/manual-note method card requires human review")
        return self


class PaperMethodCardInput(BaseModel):
    """Input for extracting a method card from local text."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_type: PaperSourceType
    source_path: Path | None = None
    source_text: str | None = None
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    requires_real_paper_review: bool = True

    @model_validator(mode="after")
    def exactly_one_source(self) -> Self:
        if (self.source_path is None) == (self.source_text is None):
            raise ValueError("provide exactly one of source_path or source_text")
        return self
