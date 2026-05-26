"""Graphviz DOT export for architecture diagrams."""

from __future__ import annotations

from turing_research_plus.architecture.models import ArchitectureDiagramSpec


def export_architecture_graphviz(spec: ArchitectureDiagramSpec) -> str:
    """Export an architecture diagram as a minimal DOT string."""

    lines = [f'digraph "{_quote(spec.diagram_id)}" {{', "  rankdir=TB;"]
    for node in spec.nodes:
        lines.append(f'  "{_quote(node.node_id)}" [label="{_quote(node.label)}"];')
    for edge in spec.edges:
        attrs = f' [label="{_quote(edge.label)}"]' if edge.label else ""
        lines.append(f'  "{_quote(edge.source)}" -> "{_quote(edge.target)}"{attrs};')
    if spec.requires_human_review:
        lines.append('  "requires_human_review" [label="requires-human-review"];')
    lines.append("}")
    return "\n".join(lines) + "\n"


def _quote(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace('"', '\\"')
