"""Edge quality reports for vault graph parity."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.edge_audit import EVIDENCE_REQUIRED_EDGES
from turing_research_plus.vault_graph.models import VaultGraph


class VaultEdgeQualityReport(BaseModel):
    """Review-only quality report for graph edges and review nodes."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    checked_edges: int = Field(ge=0)
    missing_edges: list[str] = Field(default_factory=list)
    weak_edges: list[str] = Field(default_factory=list)
    requires_review_nodes: list[str] = Field(default_factory=list)
    graph_summary: dict[str, int] = Field(default_factory=dict)
    requires_human_review: bool = True

    @property
    def release_blocker(self) -> bool:
        """Return whether edge quality has high-risk gaps."""

        return bool(self.missing_edges)


def evaluate_edge_quality(
    graph: VaultGraph,
    *,
    weak_confidence_threshold: float = 0.5,
) -> VaultEdgeQualityReport:
    """Evaluate missing and weak edges without modifying graph data."""

    missing_edges = []
    weak_edges = []
    for edge in graph.edges:
        edge_key = f"{edge.source_id}->{edge.target_id}:{edge.edge_type.value}"
        if edge.edge_type in EVIDENCE_REQUIRED_EDGES and not edge.source_refs:
            missing_edges.append(edge_key)
        if edge.confidence < weak_confidence_threshold:
            weak_edges.append(edge_key)

    return VaultEdgeQualityReport(
        graph_id=graph.graph_id,
        checked_edges=len(graph.edges),
        missing_edges=missing_edges,
        weak_edges=weak_edges,
        requires_review_nodes=[
            node.node_id for node in graph.nodes if node.requires_human_review
        ],
        graph_summary={
            "nodes": len(graph.nodes),
            "edges": len(graph.edges),
            "node_types": len(graph.node_types),
            "edge_types": len(graph.edge_types),
        },
    )


def render_edge_quality_report(report: VaultEdgeQualityReport) -> str:
    """Render edge quality report as Markdown."""

    missing_edges = [f"- `{item}`" for item in report.missing_edges] or ["- none"]
    weak_edges = [f"- `{item}`" for item in report.weak_edges] or ["- none"]
    lines = [
        f"# Vault Edge Quality: {report.graph_id}",
        "",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        f"- Requires human review: `{str(report.requires_human_review).lower()}`",
        "",
        "## Summary",
        "",
        *[f"- {key}: `{value}`" for key, value in report.graph_summary.items()],
        "",
        "## Missing Edges",
        "",
        *missing_edges,
        "",
        "## Weak Edges",
        "",
        *weak_edges,
    ]
    return "\n".join(lines) + "\n"
