from __future__ import annotations

from turing_research_plus.vault_ui.static_vault import (
    build_vault_ui_bundle,
    build_vggt_vault_ui_graph,
    render_vault_ui_html,
)


def test_static_vault_ui_renders_required_sections() -> None:
    graph = build_vggt_vault_ui_graph()
    bundle = build_vault_ui_bundle(graph, project_name="VGGT", source_markdown={})
    html = render_vault_ui_html(bundle, graph)

    assert "Concept Nodes" in html
    assert "Paper Nodes" in html
    assert "Method Nodes" in html
    assert "Artifact Nodes" in html
    assert "Claim Nodes" in html
    assert "Failure Nodes" in html
    assert "Route Nodes" in html
    assert "Missing Edges" in html
    assert "Graph is not truth" in html
    assert "vault-search-index" in html


def test_vggt_vault_ui_graph_keeps_sparseconv_unproven() -> None:
    graph = build_vggt_vault_ui_graph()

    assert graph.missing_edges
    assert any("SparseConv3D success claim lacks" in item for item in graph.missing_edges)
    assert any(node.node_id == "sparseconv_success_claim" for node in graph.nodes)
    assert all("D:/vggt" not in ref for ref in graph.source_refs)
