from __future__ import annotations

from turing_research_plus.vault_graph.models import (
    VaultGraph,
    VaultGraphEdge,
    VaultGraphEdgeType,
    VaultGraphNode,
    VaultGraphNodeType,
)


def test_vault_graph_populates_node_and_edge_types() -> None:
    graph = VaultGraph(
        graph_id="test",
        nodes=[
            VaultGraphNode(
                node_id="vggt",
                label="VGGT",
                node_type=VaultGraphNodeType.CONCEPT,
            )
        ],
        edges=[
            VaultGraphEdge(
                source_id="vggt",
                target_id="smplx",
                edge_type=VaultGraphEdgeType.RELATED_TO,
            )
        ],
    )

    assert VaultGraphNodeType.CONCEPT in graph.node_types
    assert VaultGraphEdgeType.RELATED_TO in graph.edge_types
    assert graph.model_dump(mode="json")["graph_id"] == "test"
