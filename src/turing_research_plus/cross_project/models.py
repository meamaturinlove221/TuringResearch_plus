"""Models for cross-project evidence graph comparison."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CrossProjectNodeType(StrEnum):
    """Supported cross-project graph node types."""

    PROJECT = "project"
    CLAIM = "claim"
    ARTIFACT = "artifact"
    METHOD = "method"
    FAILURE = "failure"
    ROUTE = "route"


class CrossProjectEdgeType(StrEnum):
    """Supported cross-project graph edge types."""

    SHARES_METHOD = "shares_method"
    SHARES_FAILURE = "shares_failure"
    SHARES_ARTIFACT_PATTERN = "shares_artifact_pattern"
    SHARES_ROUTE_PATTERN = "shares_route_pattern"
    REUSES_TEMPLATE = "reuses_template"
    MISSING_EVIDENCE = "missing_evidence"
    RELATED_PROJECT = "related_project"


class CrossProjectStatus(StrEnum):
    """Review status labels for cross-project graph output."""

    DRAFT = "draft"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"


class CrossProjectNode(BaseModel):
    """One node in a cross-project evidence graph."""

    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    node_type: CrossProjectNodeType
    project_id: str | None = None
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    status: CrossProjectStatus = CrossProjectStatus.REQUIRES_HUMAN_REVIEW
    requires_human_review: bool = True
    evidence_source: bool = False

    @model_validator(mode="after")
    def node_is_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("cross-project nodes require human review")
        if self.evidence_source:
            raise ValueError("cross-project nodes are not evidence sources")
        return self


class CrossProjectEdge(BaseModel):
    """One review-only relationship between cross-project graph nodes."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    edge_type: CrossProjectEdgeType
    source_projects: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=1)
    confidence: float = Field(default=0.5, ge=0, le=1)
    requires_human_review: bool = True
    evidence_transfer: bool = False

    @model_validator(mode="after")
    def edge_does_not_transfer_evidence(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("cross-project edges require human review")
        if self.evidence_transfer:
            raise ValueError("cross-project edges cannot transfer evidence")
        return self


class SharedPattern(BaseModel):
    """A shared method, failure, artifact, or route pattern."""

    model_config = ConfigDict(extra="forbid")

    pattern_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    projects: list[str] = Field(default_factory=list)
    node_ids: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    caveat: str = Field(
        default="Shared pattern is a reuse hint only, not shared evidence.",
        min_length=1,
    )
    requires_human_review: bool = True

    @model_validator(mode="after")
    def shared_patterns_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("shared patterns require human review")
        if len(set(self.projects)) != len(self.projects):
            raise ValueError("shared pattern projects must be unique")
        return self


class ReusableTemplateHint(BaseModel):
    """A conservative reusable template hint across projects."""

    model_config = ConfigDict(extra="forbid")

    template_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    applies_to_projects: list[str] = Field(default_factory=list)
    reusable_parts: list[str] = Field(default_factory=list)
    caveat: str = Field(
        default="Template reuse requires project-specific review and evidence.",
        min_length=1,
    )
    requires_human_review: bool = True

    @model_validator(mode="after")
    def reusable_templates_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("reusable template hints require human review")
        return self


class CrossProjectEvidenceGraph(BaseModel):
    """Serializable graph for comparing multiple research projects."""

    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(min_length=1)
    project_nodes: list[CrossProjectNode] = Field(default_factory=list)
    claim_nodes: list[CrossProjectNode] = Field(default_factory=list)
    artifact_nodes: list[CrossProjectNode] = Field(default_factory=list)
    method_nodes: list[CrossProjectNode] = Field(default_factory=list)
    failure_nodes: list[CrossProjectNode] = Field(default_factory=list)
    route_nodes: list[CrossProjectNode] = Field(default_factory=list)
    cross_project_edges: list[CrossProjectEdge] = Field(default_factory=list)
    shared_methods: list[SharedPattern] = Field(default_factory=list)
    shared_failures: list[SharedPattern] = Field(default_factory=list)
    reusable_templates: list[ReusableTemplateHint] = Field(default_factory=list)
    missing_evidence_claims: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    evidence_source: bool = False

    @model_validator(mode="after")
    def graph_is_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("cross-project evidence graphs require human review")
        if self.evidence_source:
            raise ValueError("cross-project graph is not an evidence source")
        return self


class CrossProjectComparison(BaseModel):
    """Structured comparison distilled from a cross-project graph."""

    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(min_length=1)
    shared_methods: list[SharedPattern] = Field(default_factory=list)
    shared_failures: list[SharedPattern] = Field(default_factory=list)
    shared_artifact_patterns: list[SharedPattern] = Field(default_factory=list)
    shared_route_patterns: list[SharedPattern] = Field(default_factory=list)
    reusable_templates: list[ReusableTemplateHint] = Field(default_factory=list)
    claims_missing_evidence: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    evidence_transfer: bool = False

    @model_validator(mode="after")
    def comparison_preserves_boundaries(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("cross-project comparisons require human review")
        if self.evidence_transfer:
            raise ValueError("cross-project comparisons cannot transfer evidence")
        return self
