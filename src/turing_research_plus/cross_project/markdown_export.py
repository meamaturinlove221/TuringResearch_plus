"""Markdown export for cross-project evidence graphs."""

from __future__ import annotations

from collections.abc import Iterable

from turing_research_plus.cross_project.comparator import compare_cross_project_graph
from turing_research_plus.cross_project.models import (
    CrossProjectEvidenceGraph,
    SharedPattern,
)


def render_cross_project_graph_markdown(graph: CrossProjectEvidenceGraph) -> str:
    """Render a cross-project evidence graph as a concise Markdown report."""

    comparison = compare_cross_project_graph(graph)
    lines = [
        f"# Cross-project Evidence Graph: {graph.workspace_id}",
        "",
        f"- Project nodes: `{len(graph.project_nodes)}`",
        f"- Claim nodes: `{len(graph.claim_nodes)}`",
        f"- Artifact nodes: `{len(graph.artifact_nodes)}`",
        f"- Method nodes: `{len(graph.method_nodes)}`",
        f"- Failure nodes: `{len(graph.failure_nodes)}`",
        f"- Route nodes: `{len(graph.route_nodes)}`",
        f"- Requires human review: `{str(graph.requires_human_review).lower()}`",
        f"- Evidence source: `{str(graph.evidence_source).lower()}`",
        "",
        "## Shared Methods",
        "",
        *_pattern_lines(graph.shared_methods),
        "",
        "## Shared Failures",
        "",
        *_pattern_lines(graph.shared_failures),
        "",
        "## Shared Artifact Patterns",
        "",
        *_pattern_lines(comparison.shared_artifact_patterns),
        "",
        "## Shared Route Patterns",
        "",
        *_pattern_lines(comparison.shared_route_patterns),
        "",
        "## Reusable Templates",
        "",
    ]
    if graph.reusable_templates:
        for template in graph.reusable_templates:
            lines.append(
                f"- `{template.template_id}`: {template.title} "
                f"({', '.join(template.applies_to_projects)})"
            )
            lines.append(f"  - Caveat: {template.caveat}")
    else:
        lines.append("- none")

    lines.extend(["", "## Claims Missing Evidence", ""])
    lines.extend([f"- `{claim}`" for claim in graph.missing_evidence_claims] or ["- none"])
    lines.extend(
        [
            "",
            "## Safety Boundary",
            "",
            "- This graph is a reusable-pattern index, not a source of evidence.",
            "- It does not transfer proof between projects.",
            "- All cross-project reuse requires human review.",
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend([f"- {limitation}" for limitation in graph.limitations] or ["- none"])
    lines.append("")
    return "\n".join(lines)


def _pattern_lines(patterns: Iterable[SharedPattern]) -> list[str]:
    items = list(patterns)
    if not items:
        return ["- none"]
    return [
        f"- `{item.pattern_id}`: {item.label} ({', '.join(item.projects)})"
        for item in items
    ]
