"""Mermaid export for architecture diagrams."""

from __future__ import annotations

from turing_research_plus.architecture.models import ArchitectureDiagramSpec


def export_architecture_mermaid(spec: ArchitectureDiagramSpec) -> str:
    """Export an architecture diagram as Mermaid flowchart TB."""

    lines = ["flowchart TB"]
    grouped_nodes = {node.node_id for node in spec.nodes if node.group}
    for group in spec.groups:
        group_nodes = [node for node in spec.nodes if _group_id(node.group) == group.group_id]
        if not group_nodes:
            continue
        lines.append(f"  subgraph {group.group_id}[{_escape(group.label)}]")
        for node in group_nodes:
            lines.append(f"    {node.node_id}[{_escape(node.label)}]")
        lines.append("  end")
    for node in spec.nodes:
        if node.node_id not in grouped_nodes:
            lines.append(f"  {node.node_id}[{_escape(node.label)}]")
    for edge in spec.edges:
        label = f" -- {_escape(edge.label)} --> " if edge.label else " --> "
        lines.append(f"  {edge.source}{label}{edge.target}")
    if spec.requires_human_review:
        lines.append("  review_notice[requires-human-review]")
    return "\n".join(lines) + "\n"


def _group_id(group: str | None) -> str | None:
    if group is None:
        return None
    return "".join(char.lower() if char.isalnum() else "_" for char in group).strip("_")


def _escape(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace("[", "(").replace("]", ")").replace("\n", " ")
