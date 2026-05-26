"""Models for lightweight vault graph enhancement."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class VaultGraphNodeType(StrEnum):
    """Supported node types."""

    PAPER = "paper"
    METHOD = "method"
    DATASET = "dataset"
    EXPERIMENT = "experiment"
    ARTIFACT = "artifact"
    CLAIM = "claim"
    FAILURE = "failure"
    ROUTE = "route"
    SKILL = "skill"
    CONCEPT = "concept"
    ARCHITECTURE_COMPONENT = "architecture_component"


class VaultGraphEdgeType(StrEnum):
    """Supported edge types."""

    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    DERIVED_FROM = "derived_from"
    CITES = "cites"
    RELATED_TO = "related_to"
    MAPS_TO = "maps_to"
    USES = "uses"
    BLOCKS = "blocks"
    REQUIRES = "requires"
    IMPROVES = "improves"
    RISKS = "risks"
    BELONGS_TO = "belongs_to"


class VaultGraphStatus(StrEnum):
    """Graph status labels."""

    DRAFT = "draft"
    REVIEW = "requires-human-review"
    READY = "ready"


class VaultGraphNode(BaseModel):
    """One graph node."""

    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    node_type: VaultGraphNodeType
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    status: VaultGraphStatus = VaultGraphStatus.REVIEW
    aliases: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class VaultGraphEdge(BaseModel):
    """One typed graph edge."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    edge_type: VaultGraphEdgeType
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    status: VaultGraphStatus = VaultGraphStatus.REVIEW
    requires_human_review: bool = True


class VaultGraph(BaseModel):
    """Serializable lightweight vault graph."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    nodes: list[VaultGraphNode] = Field(default_factory=list)
    edges: list[VaultGraphEdge] = Field(default_factory=list)
    node_types: list[VaultGraphNodeType] = Field(default_factory=list)
    edge_types: list[VaultGraphEdgeType] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0, le=1)
    status: VaultGraphStatus = VaultGraphStatus.REVIEW
    missing_edges: list[str] = Field(default_factory=list)
    dangling_edges: list[str] = Field(default_factory=list)
    wikilink_export: str | None = None

    @model_validator(mode="after")
    def populate_type_lists(self) -> VaultGraph:
        self.node_types = sorted({node.node_type for node in self.nodes}, key=str)
        self.edge_types = sorted({edge.edge_type for edge in self.edges}, key=str)
        return self


class VaultGraphAuditIssue(BaseModel):
    """One vault graph audit issue."""

    model_config = ConfigDict(extra="forbid")

    issue_type: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    node_id: str | None = None
    edge_key: str | None = None


class VaultGraphAuditReport(BaseModel):
    """Audit report for graph edges and evidence."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    checked_nodes: int = Field(ge=0)
    checked_edges: int = Field(ge=0)
    issues: list[VaultGraphAuditIssue] = Field(default_factory=list)
    missing_edges: list[str] = Field(default_factory=list)
    dangling_edges: list[str] = Field(default_factory=list)
    low_confidence_nodes: list[str] = Field(default_factory=list)
    requires_human_review_nodes: list[str] = Field(default_factory=list)

    @property
    def passed(self) -> bool:
        """Return whether no high-severity issue exists."""

        return not any(issue.severity in {"high", "critical"} for issue in self.issues)


class OntologySOPResult(BaseModel):
    """Result of one ontology SOP step."""

    model_config = ConfigDict(extra="forbid")

    sop_name: str = Field(min_length=1)
    status: VaultGraphStatus = VaultGraphStatus.REVIEW
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    required_human_review: bool = True
    notes: list[str] = Field(default_factory=list)
