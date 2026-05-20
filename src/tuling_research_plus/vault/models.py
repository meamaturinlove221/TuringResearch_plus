"""Wiki Vault models for TulingResearch Plus."""

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tuling_research_plus.artifacts.models import EvidenceRef


class VaultEntityType(StrEnum):
    """Supported vault entity types."""

    SOURCE = "source"
    CONCEPT = "concept"
    ENTITY = "entity"
    CLAIM = "claim"
    RELATION = "relation"
    QUESTION = "question"
    EVIDENCE = "evidence"
    FAILURE = "failure"
    TOPIC = "topic"


class VaultEdgeType(StrEnum):
    """Supported vault edge types."""

    COMPONENT_OF = "component_of"
    INSTANCE_OF = "instance_of"
    SUPPORTED_BY = "supported_by"
    CONTRADICTS = "contradicts"
    SUPERSEDES = "supersedes"
    DERIVED_FROM = "derived_from"
    ADDRESSES = "addresses"
    RAISES = "raises"
    FAILED_FOR = "failed_for"
    RELATED_TO = "related_to"


class VaultPage(BaseModel):
    """Markdown vault page with typed frontmatter."""

    model_config = ConfigDict(extra="forbid")

    page_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    entity_type: VaultEntityType
    body: str = ""
    evidence: list[EvidenceRef] = Field(default_factory=list)
    artifact_id: str | None = None
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def filename(self) -> str:
        return f"{self.page_id}.md"


class VaultEdge(BaseModel):
    """Typed edge between vault pages."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    edge_type: VaultEdgeType
    evidence: list[EvidenceRef] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def claim_supported_by_requires_evidence(self) -> "VaultEdge":
        if self.edge_type == VaultEdgeType.SUPPORTED_BY and not self.evidence:
            raise ValueError("supported_by edge requires evidence")
        return self

    @property
    def edge_key(self) -> tuple[str, str, VaultEdgeType]:
        return (self.source_id, self.target_id, self.edge_type)


class VaultSearchResult(BaseModel):
    """Vault search hit."""

    model_config = ConfigDict(extra="forbid")

    page_id: str
    title: str
    score: float
    path: Path


class VaultLintIssue(BaseModel):
    """Vault lint issue."""

    model_config = ConfigDict(extra="forbid")

    issue_type: str = Field(min_length=1)
    path: Path | None = None
    page_id: str | None = None
    message: str = Field(min_length=1)


class VaultGraphStats(BaseModel):
    """Vault graph statistics."""

    model_config = ConfigDict(extra="forbid")

    page_count: int = Field(ge=0)
    edge_count: int = Field(ge=0)
    orphan_count: int = Field(ge=0)


class VaultIngestResult(BaseModel):
    """Result of artifact ingestion."""

    model_config = ConfigDict(extra="forbid")

    pages: list[VaultPage] = Field(default_factory=list)
    edges: list[VaultEdge] = Field(default_factory=list)
