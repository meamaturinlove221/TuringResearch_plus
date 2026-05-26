from __future__ import annotations

from turing_research_plus.vault_graph.edge_audit import audit_vault_graph
from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphEdge,
    VaultGraphEdgeType,
    VaultGraphNode,
    VaultGraphNodeType,
)


def test_edge_audit_detects_missing_evidence_and_dangling_edge() -> None:
    graph = VaultGraph(
        graph_id="audit",
        nodes=[
            VaultGraphNode(
                node_id="claim",
                label="SparseConv3D success",
                node_type=VaultGraphNodeType.CLAIM,
                confidence=0.3,
            )
        ],
        edges=[
            VaultGraphEdge(
                source_id="claim",
                target_id="missing",
                edge_type=VaultGraphEdgeType.SUPPORTS,
            )
        ],
    )

    report = audit_vault_graph(graph)

    assert report.passed is False
    assert report.dangling_edges
    assert report.missing_edges
    assert "claim" in report.low_confidence_nodes
