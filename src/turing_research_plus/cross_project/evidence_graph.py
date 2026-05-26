"""Build cross-project evidence graphs from workspace registries."""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from turing_research_plus.cross_project.models import (
    CrossProjectEdge,
    CrossProjectEdgeType,
    CrossProjectEvidenceGraph,
    CrossProjectNode,
    CrossProjectNodeType,
    ReusableTemplateHint,
    SharedPattern,
)
from turing_research_plus.workspace.context_loader import load_workspace_context
from turing_research_plus.workspace.models import WorkspaceProject
from turing_research_plus.workspace.project_index import ProjectIndex
from turing_research_plus.workspace.registry import load_workspace_registry


def build_cross_project_graph_from_workspace(path: Path) -> CrossProjectEvidenceGraph:
    """Load a local workspace registry and build a review-only graph."""

    return build_cross_project_evidence_graph(ProjectIndex(load_workspace_registry(path)))


def build_cross_project_evidence_graph(index: ProjectIndex) -> CrossProjectEvidenceGraph:
    """Build a cross-project graph without ingesting evidence automatically."""

    project_nodes: list[CrossProjectNode] = []
    claim_nodes: list[CrossProjectNode] = []
    artifact_nodes: list[CrossProjectNode] = []
    method_nodes: list[CrossProjectNode] = []
    failure_nodes: list[CrossProjectNode] = []
    route_nodes: list[CrossProjectNode] = []

    for project in index.list_projects():
        context = load_workspace_context(project)
        loaded = context.loaded_files
        project_nodes.append(_project_node(project))
        claim_nodes.extend(_claim_nodes(project, loaded.get("evidence_ledger", "")))
        artifact_nodes.extend(_artifact_nodes(project, loaded.get("artifact_plan", "")))
        method_nodes.extend(_method_nodes(project, loaded))
        failure_nodes.extend(_failure_nodes(project, loaded))
        route_nodes.extend(_route_nodes(project, loaded.get("experiment_routes", "")))

    shared_methods = _shared_patterns("method", method_nodes)
    shared_failures = _shared_patterns("failure", failure_nodes)
    shared_artifacts = _shared_patterns("artifact", artifact_nodes)
    shared_routes = _shared_patterns("route", route_nodes)
    reusable_templates = _reusable_templates(
        shared_methods,
        shared_failures,
        shared_artifacts,
        shared_routes,
    )
    edges = _cross_project_edges(shared_methods, CrossProjectEdgeType.SHARES_METHOD)
    edges.extend(_cross_project_edges(shared_failures, CrossProjectEdgeType.SHARES_FAILURE))
    edges.extend(
        _cross_project_edges(
            shared_artifacts,
            CrossProjectEdgeType.SHARES_ARTIFACT_PATTERN,
        )
    )
    edges.extend(_cross_project_edges(shared_routes, CrossProjectEdgeType.SHARES_ROUTE_PATTERN))
    edges.extend(_template_edges(reusable_templates))

    missing_claims = [
        node.node_id
        for node in claim_nodes
        if _looks_like_missing_evidence(node.label)
    ]
    edges.extend(_missing_evidence_edges(claim_nodes))

    return CrossProjectEvidenceGraph(
        workspace_id=index.workspace.workspace_id,
        project_nodes=project_nodes,
        claim_nodes=claim_nodes,
        artifact_nodes=artifact_nodes,
        method_nodes=method_nodes,
        failure_nodes=failure_nodes,
        route_nodes=route_nodes,
        cross_project_edges=edges,
        shared_methods=shared_methods,
        shared_failures=shared_failures,
        reusable_templates=reusable_templates,
        missing_evidence_claims=missing_claims,
        limitations=[
            "Cross-project graph is a pattern index, not an evidence source.",
            "Evidence from one project is never applied to another project automatically.",
            "All reusable patterns require project-specific human review.",
        ],
        requires_human_review=True,
        evidence_source=False,
    )


def _project_node(project: WorkspaceProject) -> CrossProjectNode:
    return CrossProjectNode(
        node_id=f"project:{project.project_id}",
        label=project.project_name,
        node_type=CrossProjectNodeType.PROJECT,
        project_id=project.project_id,
        source_refs=[f"workspace://{project.project_id}"],
        confidence=0.8,
    )


def _claim_nodes(project: WorkspaceProject, evidence_text: str) -> list[CrossProjectNode]:
    nodes = []
    for index, line in enumerate(_bullet_lines(evidence_text), start=1):
        if not _looks_like_claim(line):
            continue
        nodes.append(
            CrossProjectNode(
                node_id=f"claim:{project.project_id}:{index}",
                label=line,
                node_type=CrossProjectNodeType.CLAIM,
                project_id=project.project_id,
                source_refs=[_source_ref(project, "evidence_ledger")],
                confidence=0.45 if _looks_like_missing_evidence(line) else 0.55,
            )
        )
    return nodes


def _artifact_nodes(project: WorkspaceProject, artifact_text: str) -> list[CrossProjectNode]:
    nodes = []
    for index, line in enumerate(_bullet_lines(artifact_text), start=1):
        nodes.append(
            CrossProjectNode(
                node_id=f"artifact:{project.project_id}:{index}",
                label=_artifact_pattern_label(line),
                node_type=CrossProjectNodeType.ARTIFACT,
                project_id=project.project_id,
                source_refs=[_source_ref(project, "artifact_plan")],
                confidence=0.5,
            )
        )
    return nodes


def _method_nodes(project: WorkspaceProject, loaded: dict[str, str]) -> list[CrossProjectNode]:
    text = " ".join([*loaded.values(), *project.tags, *project.notes]).lower()
    patterns = {
        "route planning": ["route", "planned"],
        "artifact review": ["artifact", "summary"],
        "visual review": ["visual", "board", "checklist"],
        "advisor review": ["advisor", "review"],
        "sparseconv3d": ["sparseconv3d"],
        "segmentation sanity review": ["segmentation"],
        "preprocessing check": ["preprocessing"],
    }
    nodes = []
    for label, terms in patterns.items():
        if any(term in text for term in terms):
            nodes.append(
                CrossProjectNode(
                    node_id=f"method:{project.project_id}:{_slug(label)}",
                    label=label,
                    node_type=CrossProjectNodeType.METHOD,
                    project_id=project.project_id,
                    source_refs=[f"workspace://{project.project_id}/method-patterns"],
                    confidence=0.45,
                )
            )
    return nodes


def _failure_nodes(project: WorkspaceProject, loaded: dict[str, str]) -> list[CrossProjectNode]:
    text = " ".join(loaded.values()).lower()
    patterns = {
        "not enough evidence": ["not-enough-evidence", "no observed", "no model performance"],
        "hard blocked": ["hard-blocked"],
        "missing artifacts": ["required future artifacts", "missing artifact"],
        "no real data": ["no real patient data", "no raw medical data"],
        "experiment not run": ["no experiment is run", "not executed", "not run"],
    }
    nodes = []
    for label, terms in patterns.items():
        if any(term in text for term in terms):
            nodes.append(
                CrossProjectNode(
                    node_id=f"failure:{project.project_id}:{_slug(label)}",
                    label=label,
                    node_type=CrossProjectNodeType.FAILURE,
                    project_id=project.project_id,
                    source_refs=[f"workspace://{project.project_id}/failure-patterns"],
                    confidence=0.55,
                )
            )
    return nodes


def _route_nodes(project: WorkspaceProject, routes_text: str) -> list[CrossProjectNode]:
    nodes = []
    if "planned" in routes_text.lower():
        nodes.append(
            CrossProjectNode(
                node_id=f"route:{project.project_id}:planned_route",
                label="planned route",
                node_type=CrossProjectNodeType.ROUTE,
                project_id=project.project_id,
                source_refs=[_source_ref(project, "experiment_routes")],
                confidence=0.55,
            )
        )
    for index, line in enumerate(_bullet_lines(routes_text), start=1):
        nodes.append(
            CrossProjectNode(
                node_id=f"route:{project.project_id}:{index}",
                label=_route_pattern_label(line),
                node_type=CrossProjectNodeType.ROUTE,
                project_id=project.project_id,
                source_refs=[_source_ref(project, "experiment_routes")],
                confidence=0.45,
            )
        )
    return nodes


def _shared_patterns(kind: str, nodes: list[CrossProjectNode]) -> list[SharedPattern]:
    grouped: dict[str, list[CrossProjectNode]] = defaultdict(list)
    for node in nodes:
        grouped[_normalize_pattern(node.label)].append(node)

    shared: list[SharedPattern] = []
    for key, items in sorted(grouped.items()):
        projects = sorted({item.project_id for item in items if item.project_id})
        if len(projects) < 2:
            continue
        shared.append(
            SharedPattern(
                pattern_id=f"{kind}:{key}",
                label=items[0].label,
                projects=projects,
                node_ids=[item.node_id for item in items],
                source_refs=sorted({ref for item in items for ref in item.source_refs}),
            )
        )
    return shared


def _cross_project_edges(
    patterns: list[SharedPattern],
    edge_type: CrossProjectEdgeType,
) -> list[CrossProjectEdge]:
    edges: list[CrossProjectEdge] = []
    for pattern in patterns:
        if len(pattern.node_ids) < 2:
            continue
        source_id = pattern.node_ids[0]
        for target_id in pattern.node_ids[1:]:
            edges.append(
                CrossProjectEdge(
                    source_id=source_id,
                    target_id=target_id,
                    edge_type=edge_type,
                    source_projects=pattern.projects,
                    rationale=(
                        f"Both projects expose `{pattern.label}` as a reusable pattern; "
                        "this is not shared evidence."
                    ),
                    confidence=0.45,
                    evidence_transfer=False,
                )
            )
    return edges


def _template_edges(templates: list[ReusableTemplateHint]) -> list[CrossProjectEdge]:
    edges: list[CrossProjectEdge] = []
    for template in templates:
        if len(template.applies_to_projects) < 2:
            continue
        source_id = f"project:{template.applies_to_projects[0]}"
        for project_id in template.applies_to_projects[1:]:
            edges.append(
                CrossProjectEdge(
                    source_id=source_id,
                    target_id=f"project:{project_id}",
                    edge_type=CrossProjectEdgeType.REUSES_TEMPLATE,
                    source_projects=template.applies_to_projects,
                    rationale=f"Potential reusable template: {template.title}.",
                    confidence=0.4,
                    evidence_transfer=False,
                )
            )
    return edges


def _missing_evidence_edges(claim_nodes: list[CrossProjectNode]) -> list[CrossProjectEdge]:
    edges = []
    for node in claim_nodes:
        if not node.project_id or not _looks_like_missing_evidence(node.label):
            continue
        edges.append(
            CrossProjectEdge(
                source_id=f"project:{node.project_id}",
                target_id=node.node_id,
                edge_type=CrossProjectEdgeType.MISSING_EVIDENCE,
                source_projects=[node.project_id],
                rationale="Claim is explicitly missing, blocked, or not enough evidence.",
                confidence=0.6,
                evidence_transfer=False,
            )
        )
    return edges


def _reusable_templates(
    shared_methods: list[SharedPattern],
    shared_failures: list[SharedPattern],
    shared_artifacts: list[SharedPattern],
    shared_routes: list[SharedPattern],
) -> list[ReusableTemplateHint]:
    templates: list[ReusableTemplateHint] = []
    all_projects = sorted(
        {
            project
            for pattern in [*shared_methods, *shared_failures, *shared_artifacts, *shared_routes]
            for project in pattern.projects
        }
    )
    if not all_projects:
        return templates
    if shared_routes:
        templates.append(
            ReusableTemplateHint(
                template_id="planned_route_review_template",
                title="Planned route review template",
                applies_to_projects=all_projects,
                reusable_parts=["route status", "hard gate placeholder", "next action"],
            )
        )
    if shared_artifacts:
        templates.append(
            ReusableTemplateHint(
                template_id="artifact_pattern_review_template",
                title="Artifact pattern review template",
                applies_to_projects=all_projects,
                reusable_parts=["small summary", "visual checklist", "manifest/hash policy"],
            )
        )
    if shared_failures:
        templates.append(
            ReusableTemplateHint(
                template_id="missing_evidence_review_template",
                title="Missing evidence review template",
                applies_to_projects=all_projects,
                reusable_parts=["missing evidence label", "required action", "review owner"],
            )
        )
    return templates


def _bullet_lines(text: str) -> list[str]:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("- "):
            lines.append(line[2:].strip().rstrip(";"))
    return lines


def _looks_like_claim(line: str) -> bool:
    lowered = line.lower()
    return any(
        term in lowered
        for term in [
            "evidence",
            "success",
            "claim",
            "performance",
            "result",
            "blocked",
            "review",
        ]
    )


def _looks_like_missing_evidence(label: str) -> bool:
    lowered = label.lower()
    return any(
        term in lowered
        for term in [
            "not-enough-evidence",
            "not established",
            "no observed",
            "no model performance",
            "hard-blocked",
            "requires human review",
            "requires-real-experiment",
        ]
    )


def _artifact_pattern_label(line: str) -> str:
    lowered = line.lower()
    if "summary" in lowered or "table" in lowered:
        return "summary artifact"
    if "visual" in lowered or "board" in lowered or "checklist" in lowered:
        return "visual review artifact"
    if "manifest" in lowered or "sha256" in lowered:
        return "manifest artifact"
    if "cleanup" in lowered:
        return "cleanup report"
    if "raw" in lowered:
        return "raw data omission"
    return _clean_label(line)


def _route_pattern_label(line: str) -> str:
    lowered = line.lower()
    if "planned" in lowered:
        return "planned route"
    if "advisor" in lowered:
        return "advisor summary route"
    if "preprocessing" in lowered:
        return "preprocessing check route"
    if "segmentation" in lowered:
        return "segmentation sanity review route"
    return _clean_label(line)


def _source_ref(project: WorkspaceProject, label: str) -> str:
    return f"workspace://{project.project_id}/{label}"


def _normalize_pattern(label: str) -> str:
    return _slug(label)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "unknown"


def _clean_label(value: str) -> str:
    return value.strip().rstrip(".")
