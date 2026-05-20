"""SOP graph boundary models for TulingResearch Plus."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SOPGraphType(StrEnum):
    """Supported SOP graph types."""

    CAMPAIGN = "campaign"
    FEATURE = "feature"
    PAPER = "paper"
    EXPERIMENT = "experiment"
    RELEASE = "release"


class SOPNodeKind(StrEnum):
    """Supported SOP graph node kinds."""

    STEP = "step"
    ARTIFACT = "artifact"
    TOOL = "tool"
    QUALITY_GATE = "quality_gate"
    FAILURE_GATE = "failure_gate"


class SOPNode(BaseModel):
    """One SOP graph node."""

    model_config = ConfigDict(extra="forbid")

    node_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    kind: SOPNodeKind = SOPNodeKind.STEP


class SOPEdge(BaseModel):
    """One directed SOP graph edge."""

    model_config = ConfigDict(extra="forbid")

    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    label: str | None = None


class SOPGraph(BaseModel):
    """A fully specified SOP graph."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    graph_type: SOPGraphType
    title: str = Field(min_length=1)
    nodes: list[SOPNode] = Field(min_length=1)
    edges: list[SOPEdge] = Field(default_factory=list)
    input_artifacts: list[str] = Field(default_factory=list)
    output_artifacts: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    quality_gates: list[str] = Field(min_length=1)
    failure_gates: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_edges(self) -> "SOPGraph":
        node_ids = {node.node_id for node in self.nodes}
        for edge in self.edges:
            if edge.source not in node_ids or edge.target not in node_ids:
                msg = f"edge {edge.source}->{edge.target} references unknown node"
                raise ValueError(msg)
        return self


class SOPGenerationRequest(BaseModel):
    """Generic request for paper.sop_graph_generate."""

    model_config = ConfigDict(extra="forbid")

    graph_type: SOPGraphType
    title: str = Field(min_length=1)
    source_id: str = Field(default="manual", min_length=1)
    input_artifacts: list[str] = Field(default_factory=list)
    output_artifacts: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    quality_gates: list[str] = Field(default_factory=list)
    failure_gates: list[str] = Field(default_factory=list)
    include_skill_skeleton: bool = False
    include_codex_prompt: bool = False


class SOPGenerationResult(BaseModel):
    """Generated SOP graph artifacts."""

    model_config = ConfigDict(extra="forbid")

    graph: SOPGraph
    mermaid_text: str = Field(min_length=1)
    sop_markdown: str = Field(min_length=1)
    skill_skeleton: str | None = None
    codex_prompt: str | None = None
