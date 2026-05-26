"""Graph view helpers for static vault UI."""

from __future__ import annotations

import html

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.vault_graph.models import VaultGraph, VaultGraphEdge, VaultGraphNode


class VaultGraphView(BaseModel):
    """A render-ready graph view."""

    model_config = ConfigDict(extra="forbid")

    graph_id: str = Field(min_length=1)
    nodes: list[VaultGraphNode] = Field(default_factory=list)
    edges: list[VaultGraphEdge] = Field(default_factory=list)
    missing_edges: list[str] = Field(default_factory=list)
    requires_review_nodes: list[str] = Field(default_factory=list)
    graph_not_truth: bool = True
    requires_human_review: bool = True


def build_vault_graph_view(graph: VaultGraph) -> VaultGraphView:
    """Build a simple graph view from a vault graph."""

    requires_review_nodes = [
        node.node_id for node in graph.nodes if node.requires_human_review
    ]
    return VaultGraphView(
        graph_id=graph.graph_id,
        nodes=graph.nodes,
        edges=graph.edges,
        missing_edges=graph.missing_edges,
        requires_review_nodes=requires_review_nodes,
    )


def render_vault_graph_view_html(view: VaultGraphView) -> str:
    """Render nodes and edges as static HTML lists."""

    node_items = "\n".join(_render_node(node) for node in view.nodes)
    edge_items = "\n".join(_render_edge(edge) for edge in view.edges) or "<li>none</li>"
    missing = "\n".join(f"<li>{html.escape(item)}</li>" for item in view.missing_edges)
    if not missing:
        missing = "<li>none recorded</li>"
    review = "\n".join(
        f"<li><a href=\"#node-{html.escape(node_id)}\">{html.escape(node_id)}</a></li>"
        for node_id in view.requires_review_nodes
    )
    if not review:
        review = "<li>none</li>"
    return f"""<section id="graph-view">
  <h2>Graph View</h2>
  <p class="boundary">Graph view is review material, not final truth.</p>
  <h3>Nodes</h3>
  <ul class="node-list">{node_items}</ul>
  <h3>Edges</h3>
  <ul>{edge_items}</ul>
  <h3>Missing Edges</h3>
  <ul>{missing}</ul>
  <h3>Requires Review Nodes</h3>
  <ul>{review}</ul>
</section>"""


def _render_node(node: VaultGraphNode) -> str:
    return (
        f'<li id="node-{html.escape(node.node_id)}">'
        f"<strong>{html.escape(node.label)}</strong> "
        f"<span class=\"badge\">{html.escape(node.node_type)}</span> "
        f"confidence={node.confidence:.2f} "
        f"status=<code>{html.escape(node.status)}</code>"
        "</li>"
    )


def _render_edge(edge: VaultGraphEdge) -> str:
    refs = ", ".join(edge.source_refs) if edge.source_refs else "missing source refs"
    return (
        "<li>"
        f"<code>{html.escape(edge.source_id)}</code> "
        f"-- <code>{html.escape(edge.edge_type)}</code> --> "
        f"<code>{html.escape(edge.target_id)}</code> "
        f"(refs: {html.escape(refs)})"
        "</li>"
    )
