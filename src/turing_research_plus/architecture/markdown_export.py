"""Markdown export for architecture diagrams."""

from __future__ import annotations

from turing_research_plus.architecture.mermaid_export import export_architecture_mermaid
from turing_research_plus.architecture.models import ArchitectureDiagramSpec


def export_architecture_markdown(spec: ArchitectureDiagramSpec) -> str:
    """Render an architecture diagram spec as Markdown."""

    lines = [
        f"# Architecture Diagram: {spec.title}",
        "",
        f"- Diagram ID: `{spec.diagram_id}`",
        f"- Source type: `{spec.source_type.value}`",
        f"- Source ref: `{spec.source_ref}`",
        f"- Requires human review: {str(spec.requires_human_review).lower()}",
        "",
        "```mermaid",
        export_architecture_mermaid(spec).rstrip(),
        "```",
        "",
        "## Mapping Notes",
        "",
        *_items(spec.mapping_notes),
        "",
        "## Limitations",
        "",
        *_items(spec.limitations),
    ]
    return "\n".join(lines) + "\n"


def _items(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- none recorded"]
