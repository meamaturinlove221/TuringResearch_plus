"""Ontology gap detection for lightweight vault graphs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphEdgeType,
    VaultGraphNodeType,
)

HIERARCHY_NODE_TYPES = {
    VaultGraphNodeType.CONCEPT,
    VaultGraphNodeType.METHOD,
    VaultGraphNodeType.DATASET,
    VaultGraphNodeType.EXPERIMENT,
}


class OntologyGap(BaseModel):
    """One ontology gap that requires review."""

    model_config = ConfigDict(extra="forbid")

    gap_type: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    node_id: str | None = None
    edge_key: str | None = None


class OntologyGapReport(BaseModel):
    """Review-only ontology gap report."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    gaps: list[OntologyGap] = Field(default_factory=list)
    missing_source_ref_nodes: list[str] = Field(default_factory=list)
    orphan_nodes: list[str] = Field(default_factory=list)
    low_confidence_nodes: list[str] = Field(default_factory=list)
    missing_hierarchy_edges: list[str] = Field(default_factory=list)
    dangling_edges: list[str] = Field(default_factory=list)
    requires_human_review_nodes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether high-risk gaps remain."""

        return any(gap.severity in {"high", "critical"} for gap in self.gaps)


def detect_ontology_gaps(
    graph: VaultGraph,
    *,
    low_confidence_threshold: float = 0.5,
) -> OntologyGapReport:
    """Detect ontology gaps without mutating the graph."""

    node_ids = {node.node_id for node in graph.nodes}
    connected_ids = {
        item
        for edge in graph.edges
        for item in (edge.source_id, edge.target_id)
        if item in node_ids
    }
    hierarchy_connected = {
        item
        for edge in graph.edges
        if edge.edge_type == VaultGraphEdgeType.BELONGS_TO
        for item in (edge.source_id, edge.target_id)
    }

    missing_source_ref_nodes = [
        node.node_id for node in graph.nodes if not node.source_refs
    ]
    orphan_nodes = [node.node_id for node in graph.nodes if node.node_id not in connected_ids]
    low_confidence_nodes = [
        node.node_id for node in graph.nodes if node.confidence < low_confidence_threshold
    ]
    missing_hierarchy_edges = [
        node.node_id
        for node in graph.nodes
        if node.node_type in HIERARCHY_NODE_TYPES
        and node.node_id not in hierarchy_connected
    ]
    dangling_edges = [
        f"{edge.source_id}->{edge.target_id}:{edge.edge_type.value}"
        for edge in graph.edges
        if edge.source_id not in node_ids or edge.target_id not in node_ids
    ]

    gaps: list[OntologyGap] = []
    gaps.extend(
        OntologyGap(
            gap_type="missing_source_refs",
            severity="high",
            message="node has no source references",
            node_id=node_id,
        )
        for node_id in missing_source_ref_nodes
    )
    gaps.extend(
        OntologyGap(
            gap_type="orphan_node",
            severity="medium",
            message="node has no graph edges",
            node_id=node_id,
        )
        for node_id in orphan_nodes
    )
    gaps.extend(
        OntologyGap(
            gap_type="low_confidence_node",
            severity="medium",
            message="node confidence is below review threshold",
            node_id=node_id,
        )
        for node_id in low_confidence_nodes
    )
    gaps.extend(
        OntologyGap(
            gap_type="missing_hierarchy_edge",
            severity="low",
            message="node has no belongs_to hierarchy edge",
            node_id=node_id,
        )
        for node_id in missing_hierarchy_edges
    )
    gaps.extend(
        OntologyGap(
            gap_type="dangling_edge",
            severity="high",
            message="edge references a missing node",
            edge_key=edge_key,
        )
        for edge_key in dangling_edges
    )

    return OntologyGapReport(
        graph_id=graph.graph_id,
        gaps=gaps,
        missing_source_ref_nodes=missing_source_ref_nodes,
        orphan_nodes=orphan_nodes,
        low_confidence_nodes=low_confidence_nodes,
        missing_hierarchy_edges=missing_hierarchy_edges,
        dangling_edges=dangling_edges,
        requires_human_review_nodes=[
            node.node_id for node in graph.nodes if node.requires_human_review
        ],
    )


def render_ontology_gap_report(report: OntologyGapReport) -> str:
    """Render ontology gaps as Markdown."""

    gap_lines = [
        f"- `{gap.gap_type}` ({gap.severity}): {gap.node_id or gap.edge_key}"
        for gap in report.gaps
    ] or ["- none"]
    lines = [
        f"# Ontology Gap Report: {report.graph_id}",
        "",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Gaps",
        "",
        *gap_lines,
    ]
    return "\n".join(lines) + "\n"
