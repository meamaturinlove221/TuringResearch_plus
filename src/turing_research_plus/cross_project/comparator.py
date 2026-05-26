"""Compare reusable patterns in a cross-project evidence graph."""

from __future__ import annotations

from collections import defaultdict

from turing_research_plus.cross_project.models import (
    CrossProjectComparison,
    CrossProjectEvidenceGraph,
    CrossProjectNode,
    SharedPattern,
)


def compare_cross_project_graph(graph: CrossProjectEvidenceGraph) -> CrossProjectComparison:
    """Build a conservative comparison report from a cross-project graph."""

    return CrossProjectComparison(
        workspace_id=graph.workspace_id,
        shared_methods=graph.shared_methods,
        shared_failures=graph.shared_failures,
        shared_artifact_patterns=_shared_node_patterns("artifact", graph.artifact_nodes),
        shared_route_patterns=_shared_node_patterns("route", graph.route_nodes),
        reusable_templates=graph.reusable_templates,
        claims_missing_evidence=graph.missing_evidence_claims,
        notes=[
            "Reusable patterns are hints only.",
            "Do not apply evidence from one project to another project automatically.",
            "Every cross-project claim requires human review.",
        ],
        requires_human_review=True,
        evidence_transfer=False,
    )


def _shared_node_patterns(kind: str, nodes: list[CrossProjectNode]) -> list[SharedPattern]:
    grouped: dict[str, list[CrossProjectNode]] = defaultdict(list)
    for node in nodes:
        grouped[node.label.lower()].append(node)

    patterns = []
    for label, items in sorted(grouped.items()):
        projects = sorted({item.project_id for item in items if item.project_id})
        if len(projects) < 2:
            continue
        patterns.append(
            SharedPattern(
                pattern_id=f"{kind}:{label.replace(' ', '_')}",
                label=items[0].label,
                projects=projects,
                node_ids=[item.node_id for item in items],
                source_refs=sorted({ref for item in items for ref in item.source_refs}),
            )
        )
    return patterns
