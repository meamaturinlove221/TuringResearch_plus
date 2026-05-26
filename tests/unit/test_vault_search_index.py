from __future__ import annotations

from turing_research_plus.vault_graph.models import VaultGraphNodeType
from turing_research_plus.vault_ui.search_index import build_vault_search_index
from turing_research_plus.vault_ui.static_vault import build_vggt_vault_ui_graph


def test_vault_search_index_covers_all_nodes() -> None:
    graph = build_vggt_vault_ui_graph()
    index = build_vault_search_index(graph)

    assert len(index) == len(graph.nodes)
    assert any(entry.title == "SparseConv3D" for entry in index)
    assert any(entry.node_type == VaultGraphNodeType.CLAIM for entry in index)
    assert all(entry.requires_human_review for entry in index)
