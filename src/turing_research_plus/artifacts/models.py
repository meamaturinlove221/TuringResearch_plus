"""Research artifact and evidence boundary models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ArtifactKind(StrEnum):
    """Stable artifact kinds emitted by TulingResearch Plus workflows."""

    NOTE = "note"
    PDF_MARKDOWN = "pdf_markdown"
    IDEA_CARD = "idea_card"
    FEATURE_CAPSULE = "feature_capsule"
    EXPERIMENT_REPORT = "experiment_report"
    ARTICLE_BLOCK = "article_block"
    DRAFT = "draft"
    WORKFLOW_STATE = "workflow_state"


class EvidenceRef(BaseModel):
    """Reference to evidence supporting a workflow claim."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    quote: str = Field(min_length=1)
    url: str | None = None
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class ResearchArtifact(BaseModel):
    """Important output produced by a workflow."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    kind: ArtifactKind
    title: str = Field(min_length=1)
    created_by: str = Field(min_length=1)
    content: dict[str, Any] = Field(default_factory=dict)
    evidence: list[EvidenceRef] = Field(min_length=1)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
