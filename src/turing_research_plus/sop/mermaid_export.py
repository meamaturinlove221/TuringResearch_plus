"""Mermaid export helpers for SOP graphs."""

from __future__ import annotations

import re

from tuling_research_plus.sop.models import SOPGraph, SOPNodeKind


def export_mermaid(graph: SOPGraph) -> str:
    """Render an SOP graph as Mermaid flowchart text."""

    lines = ["flowchart TD"]
    for node in graph.nodes:
        lines.append(f"    {_node_id(node.node_id)}{_shape(node.kind, node.label)}")
    for edge in graph.edges:
        source = _node_id(edge.source)
        target = _node_id(edge.target)
        if edge.label:
            lines.append(f"    {source} -- {edge.label} --> {target}")
        else:
            lines.append(f"    {source} --> {target}")
    return "\n".join(lines) + "\n"


def export_sop_markdown(graph: SOPGraph, mermaid_text: str) -> str:
    """Render an SOP graph as a compact Markdown SOP document."""

    lines = [
        f"# TulingResearch Plus SOP: {graph.title}",
        "",
        f"- Graph ID: `{graph.graph_id}`",
        f"- Graph type: `{graph.graph_type}`",
        "",
        "## Mermaid",
        "",
        "```mermaid",
        mermaid_text.rstrip(),
        "```",
        "",
        "## Inputs",
    ]
    lines.extend(f"- `{artifact}`" for artifact in graph.input_artifacts)
    lines.extend(["", "## Outputs"])
    lines.extend(f"- `{artifact}`" for artifact in graph.output_artifacts)
    lines.extend(["", "## Tools"])
    lines.extend(f"- `{tool}`" for tool in graph.tools)
    lines.extend(["", "## Quality Gates"])
    lines.extend(f"- {gate}" for gate in graph.quality_gates)
    lines.extend(["", "## Failure Gates"])
    lines.extend(f"- {gate}" for gate in graph.failure_gates)
    return "\n".join(lines) + "\n"


def _node_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", value)
    if cleaned and cleaned[0].isdigit():
        return f"N{cleaned}"
    return cleaned or "node"


def _shape(kind: SOPNodeKind, label: str) -> str:
    escaped = label.replace('"', "'")
    if kind == SOPNodeKind.ARTIFACT:
        return f'[("{escaped}")]'
    if kind == SOPNodeKind.TOOL:
        return f'(["{escaped}"])'
    if kind == SOPNodeKind.QUALITY_GATE:
        return f'{{"{escaped}"}}'
    if kind == SOPNodeKind.FAILURE_GATE:
        return f'{{{{"{escaped}"}}}}'
    return f'["{escaped}"]'
