"""Vault graph edge audit."""

from __future__ import annotations

from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphAuditIssue,
    VaultGraphAuditReport,
    VaultGraphEdgeType,
)

EVIDENCE_REQUIRED_EDGES = {
    VaultGraphEdgeType.SUPPORTS,
    VaultGraphEdgeType.CONTRADICTS,
    VaultGraphEdgeType.DERIVED_FROM,
    VaultGraphEdgeType.CITES,
}


def audit_vault_graph(graph: VaultGraph) -> VaultGraphAuditReport:
    """Audit dangling edges, missing evidence, and low-confidence nodes."""

    node_ids = {node.node_id for node in graph.nodes}
    issues: list[VaultGraphAuditIssue] = []
    dangling_edges: list[str] = []
    missing_edges: list[str] = []

    for edge in graph.edges:
        edge_key = f"{edge.source_id}->{edge.target_id}:{edge.edge_type}"
        if edge.source_id not in node_ids or edge.target_id not in node_ids:
            dangling_edges.append(edge_key)
            issues.append(
                VaultGraphAuditIssue(
                    issue_type="dangling_edge",
                    severity="high",
                    message="edge references a missing node",
                    edge_key=edge_key,
                )
            )
        if edge.edge_type in EVIDENCE_REQUIRED_EDGES and not edge.source_refs:
            missing_edges.append(edge_key)
            issues.append(
                VaultGraphAuditIssue(
                    issue_type="missing_evidence",
                    severity="high",
                    message="evidence-bearing edge has no source_refs",
                    edge_key=edge_key,
                )
            )

    low_confidence_nodes = [node.node_id for node in graph.nodes if node.confidence < 0.5]
    requires_review_nodes = [node.node_id for node in graph.nodes if node.requires_human_review]
    for node in graph.nodes:
        if node.confidence < 0.5:
            issues.append(
                VaultGraphAuditIssue(
                    issue_type="low_confidence_node",
                    severity="medium",
                    message="node confidence is below review threshold",
                    node_id=node.node_id,
                )
            )
    return VaultGraphAuditReport(
        graph_id=graph.graph_id,
        checked_nodes=len(graph.nodes),
        checked_edges=len(graph.edges),
        issues=issues,
        missing_edges=missing_edges,
        dangling_edges=dangling_edges,
        low_confidence_nodes=low_confidence_nodes,
        requires_human_review_nodes=requires_review_nodes,
    )
