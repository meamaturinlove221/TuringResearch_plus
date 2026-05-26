from __future__ import annotations

from turing_research_plus.vault_graph.edge_builder import build_edge
from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdgeType
from turing_research_plus.vault_graph.node_builder import build_concept_node
from turing_research_plus.vault_graph.wikilink_export import export_wikilink_summary, wikilink


def test_wikilink_helper_and_summary() -> None:
    graph = VaultGraph(
        graph_id="wiki",
        nodes=[build_concept_node("vggt", "VGGT"), build_concept_node("smplx", "SMPL-X")],
        edges=[build_edge("smplx", "vggt", VaultGraphEdgeType.MAPS_TO)],
    )

    assert wikilink("VGGT") == "[[VGGT]]"
    markdown = export_wikilink_summary(graph)
    assert "[[VGGT]]" in markdown
    assert "`maps_to`" in markdown
