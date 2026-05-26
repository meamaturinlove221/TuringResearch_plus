from __future__ import annotations

from turing_research_plus.vault_graph.backlink_index import (
    build_backlink_index,
    render_backlink_index,
)
from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node


def test_backlink_index_tracks_incoming_outgoing_and_dangling_targets() -> None:
    graph = VaultGraph(
        graph_id="vault-links",
        nodes=[
            build_concept_node("vggt", "VGGT"),
            build_concept_node("human-prior", "Human Prior"),
            build_concept_node("claim", "Claim Node"),
        ],
        edges=[
            build_edge("human-prior", "vggt", VaultGraphEdgeType.RELATED_TO),
            build_edge("claim", "vggt", VaultGraphEdgeType.SUPPORTS, source_refs=["demo"]),
            build_edge("claim", "missing-node", VaultGraphEdgeType.RELATED_TO),
        ],
    )

    index = build_backlink_index(graph)
    entries = index.by_node_id()

    assert entries["vggt"].backlinks == ["claim", "human-prior"]
    assert entries["claim"].outgoing_links == ["missing-node", "vggt"]
    assert index.dangling_targets == ["missing-node"]
    assert index.requires_human_review is True

    markdown = render_backlink_index(index)
    assert "`human-prior`" in markdown
    assert "`missing-node`" in markdown
