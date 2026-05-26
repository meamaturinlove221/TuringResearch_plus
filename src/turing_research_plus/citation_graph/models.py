"""Models for beta citation graph expansion."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CitationGraphEdgeType(StrEnum):
    """Supported citation graph edge types."""

    CITES = "cites"
    CITED_BY = "cited_by"
    RELATED = "related"
    SAME_AUTHOR = "same_author"
    RECOMMENDED = "recommended"
    MANUAL_RELATED = "manual_related"


class CitationGraphRetrievalStatus(StrEnum):
    """Graph retrieval status."""

    FAKE = "fake"
    MANUAL = "manual"
    RETRIEVED = "retrieved"
    PARTIAL = "partial"
    ERROR = "error"


class CitationGraphSourceAdapter(StrEnum):
    """Source adapter used to construct the graph."""

    FAKE = "fake_semantic_scholar"
    MANUAL = "manual_seed_list"
    LIVE_SEMANTIC_SCHOLAR = "live_semantic_scholar"


class CitationGraphTopic(StrEnum):
    """VGGT related seed topics for beta planning."""

    VGGT = "VGGT"
    SMPL_X = "SMPL-X"
    NEURALBODY = "NeuralBody"
    HUMANRAM = "HumanRAM"
    HART = "HART"
    VGGT_HPE = "VGGT-HPE"
    HGGT = "HGGT"
    FUS3D = "Fus3D"
    SPARSECONV3D = "SparseConv3D"
    HUMAN_PRIOR = "human prior"


class CitationGraphFilters(BaseModel):
    """Citation expansion filters."""

    model_config = ConfigDict(extra="forbid")

    min_year: int | None = None
    max_year: int | None = None
    open_access_only: bool = False
    min_citation_count: int | None = Field(default=None, ge=0)


class CitationGraphNode(BaseModel):
    """Paper node in the beta citation graph."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    year: int | None = None
    authors: list[str] = Field(default_factory=list)
    citation_count: int = Field(default=0, ge=0)
    is_open_access: bool = False
    topics: list[str] = Field(default_factory=list)
    source_metadata: dict[str, Any] = Field(default_factory=dict)
    human_verified: bool = False


class CitationGraphEdge(BaseModel):
    """Typed edge between citation graph nodes."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    target_id: str = Field(min_length=1)
    edge_type: CitationGraphEdgeType
    evidence: str | None = None


class CitationGraphRequest(BaseModel):
    """Input for citation graph expansion."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(default="vggt-related-work-fake", min_length=1)
    seed_papers: list[CitationGraphNode] = Field(default_factory=list)
    seed_topics: list[str] = Field(default_factory=list)
    manual_edges: list[CitationGraphEdge] = Field(default_factory=list)
    expansion_depth: int = Field(default=1, ge=0, le=3)
    max_nodes: int = Field(default=25, ge=1)
    filters: CitationGraphFilters = Field(default_factory=CitationGraphFilters)
    source_adapter: CitationGraphSourceAdapter = CitationGraphSourceAdapter.FAKE
    live_enabled: bool = False
    dry_run: bool = True


class CitationGraph(BaseModel):
    """Serializable citation graph output."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    seed_papers: list[CitationGraphNode] = Field(default_factory=list)
    nodes: list[CitationGraphNode] = Field(default_factory=list)
    edges: list[CitationGraphEdge] = Field(default_factory=list)
    frontier_nodes: list[CitationGraphNode] = Field(default_factory=list)
    expansion_depth: int = Field(default=0, ge=0)
    filters: CitationGraphFilters = Field(default_factory=CitationGraphFilters)
    source_adapter: CitationGraphSourceAdapter
    retrieval_status: CitationGraphRetrievalStatus
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def dedupe_nodes_and_edges(self) -> CitationGraph:
        node_map = {node.paper_id: node for node in self.nodes}
        self.nodes = list(node_map.values())

        edge_map: dict[tuple[str, str, CitationGraphEdgeType], CitationGraphEdge] = {}
        for edge in self.edges:
            edge_map[(edge.source_id, edge.target_id, edge.edge_type)] = edge
        self.edges = list(edge_map.values())
        return self
