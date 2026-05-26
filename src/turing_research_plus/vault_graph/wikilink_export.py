"""Markdown and wikilink export for vault graphs."""

from __future__ import annotations

from turing_research_plus.vault_graph.models import VaultGraph


def wikilink(label: str) -> str:
    """Return an inline wikilink label."""

    return f"[[{label}]]"


def export_wikilink_summary(graph: VaultGraph) -> str:
    """Export a graph summary with optional inline wikilinks."""

    labels = {node.node_id: node.label for node in graph.nodes}
    lines = [
        f"# Vault Graph: {graph.graph_id}",
        "",
        "## Nodes",
    ]
    for node in graph.nodes:
        lines.append(f"- {wikilink(node.label)} (`{node.node_type}` confidence={node.confidence})")
    lines.extend(["", "## Edges"])
    for edge in graph.edges:
        source = wikilink(labels.get(edge.source_id, edge.source_id))
        target = wikilink(labels.get(edge.target_id, edge.target_id))
        lines.append(f"- {source} -- `{edge.edge_type}` --> {target}")
    lines.append("")
    return "\n".join(lines)
