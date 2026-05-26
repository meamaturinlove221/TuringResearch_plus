"""Models for text architecture diagrams."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ArchitectureSourceType(StrEnum):
    """Supported diagram input source types."""

    METHOD_CARD = "method_card"
    EXPERIMENT_ROUTE = "experiment_route"
    FIXTURE = "derived-from-fixture"


class ArchitectureExportFormat(StrEnum):
    """Supported text export formats."""

    MERMAID = "mermaid"
    GRAPHVIZ = "graphviz"
    MARKDOWN = "markdown"


class ArchitectureNode(BaseModel):
    """One diagram node."""

    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    group: str | None = None
    node_type: str = Field(default="component", min_length=1)


class ArchitectureEdge(BaseModel):
    """One diagram edge."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    label: str | None = None
    supported: bool = True
    warning: str | None = None


class ArchitectureGroup(BaseModel):
    """One optional diagram grouping."""

    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(min_length=1)
    label: str = Field(min_length=1)


class ArchitectureDiagramSpec(BaseModel):
    """Text architecture diagram specification."""

    model_config = ConfigDict(extra="forbid")

    diagram_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    source_type: ArchitectureSourceType
    source_ref: str = Field(min_length=1)
    nodes: list[ArchitectureNode] = Field(min_length=1)
    edges: list[ArchitectureEdge] = Field(default_factory=list)
    groups: list[ArchitectureGroup] = Field(default_factory=list)
    inputs: list[str] = Field(default_factory=list)
    outputs: list[str] = Field(default_factory=list)
    mapping_notes: list[str] = Field(default_factory=list)
    export_formats: list[ArchitectureExportFormat] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def validate_edges_and_review(self) -> Self:
        node_ids = {node.node_id for node in self.nodes}
        invalid_edges = [
            f"{edge.source}->{edge.target}"
            for edge in self.edges
            if edge.source not in node_ids or edge.target not in node_ids
        ]
        if invalid_edges:
            raise ValueError(f"edges reference unknown nodes: {', '.join(invalid_edges)}")
        if self.source_type == ArchitectureSourceType.FIXTURE and not self.requires_human_review:
            raise ValueError("fixture-derived architecture diagrams require human review")
        if any(not edge.supported for edge in self.edges) and not self.requires_human_review:
            raise ValueError("unsupported edges require human review")
        return self
