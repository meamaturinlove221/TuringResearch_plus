from __future__ import annotations

from turing_research_plus.vault_ui.graph_view import (
    build_vault_graph_view,
    render_vault_graph_view_html,
)
from turing_research_plus.vault_ui.static_vault import build_vggt_vault_ui_graph


def test_vault_graph_view_exposes_missing_and_review_nodes() -> None:
    graph = build_vggt_vault_ui_graph()
    view = build_vault_graph_view(graph)

    assert view.graph_not_truth is True
    assert "sparseconv3d" in view.requires_review_nodes
    assert view.missing_edges == graph.missing_edges


def test_vault_graph_view_html_is_static_review_material() -> None:
    html = render_vault_graph_view_html(build_vault_graph_view(build_vggt_vault_ui_graph()))

    assert "Graph view is review material, not final truth." in html
    assert "requires-real-experiment" not in html
    assert "missing source refs" in html
