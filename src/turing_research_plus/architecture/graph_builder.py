"""Build text architecture diagrams from method cards or route specs."""

from __future__ import annotations

import re

from turing_research_plus.architecture.models import (
    ArchitectureDiagramSpec,
    ArchitectureEdge,
    ArchitectureExportFormat,
    ArchitectureGroup,
    ArchitectureNode,
    ArchitectureSourceType,
)
from turing_research_plus.experiment_route.models import ExperimentRouteSpec
from turing_research_plus.paper_method.models import PaperMethodCard


def build_architecture_from_method_card(
    card: PaperMethodCard,
    *,
    diagram_id: str | None = None,
) -> ArchitectureDiagramSpec:
    """Build a conservative architecture draft from a PaperMethodCard."""

    nodes: list[ArchitectureNode] = []
    nodes.extend(_nodes_from_items(card.inputs, "input", "Inputs"))
    nodes.extend(_nodes_from_items(card.architecture_components, "component", "Method Components"))
    nodes.extend(_nodes_from_items(card.outputs, "output", "Outputs"))
    if not nodes:
        nodes.append(
            ArchitectureNode(
                node_id="requires_review",
                label="requires-real-paper-review",
                group="Review",
            )
        )
    edges = _chain_edges(nodes, "method flow")
    return ArchitectureDiagramSpec(
        diagram_id=diagram_id or f"{_slug(card.paper_id)}_architecture",
        title=f"{card.title} Architecture Mapping",
        source_type=ArchitectureSourceType.FIXTURE
        if card.requires_human_review
        else ArchitectureSourceType.METHOD_CARD,
        source_ref=card.paper_id,
        nodes=nodes,
        edges=edges,
        groups=_groups_for(nodes),
        inputs=card.inputs,
        outputs=card.outputs,
        mapping_notes=[
            f"SMPL / SMPL-X role: {card.mapping_to_vggt.smpl_role}",
            f"voxel / sparseconv: {card.mapping_to_vggt.voxel_sparseconv_relevance}",
            f"tri-plane: {card.mapping_to_vggt.triplane_relevance}",
            f"token alignment: {card.mapping_to_vggt.token_alignment_relevance}",
            f"geometry output: {card.mapping_to_vggt.geometry_output_relevance}",
            "Diagram is derived from fixture or method card text, not image understanding.",
        ],
        export_formats=[
            ArchitectureExportFormat.MERMAID,
            ArchitectureExportFormat.GRAPHVIZ,
            ArchitectureExportFormat.MARKDOWN,
        ],
        limitations=[
            *card.limitations,
            "derived-from-fixture / requires-human-review",
            "No image model or third-party drawing API was used.",
        ],
        requires_human_review=True,
    )


def build_architecture_from_route(route: ExperimentRouteSpec) -> ArchitectureDiagramSpec:
    """Build a route architecture draft from an ExperimentRouteSpec."""

    nodes = [
        ArchitectureNode(node_id=_slug(stage.id), label=stage.name, group="Route Stages")
        for stage in route.stages
    ]
    edges = _chain_edges(nodes, "then")
    return ArchitectureDiagramSpec(
        diagram_id=f"{_slug(route.route_id)}_architecture",
        title=f"{route.route_id} Route Architecture",
        source_type=ArchitectureSourceType.EXPERIMENT_ROUTE,
        source_ref=route.route_id,
        nodes=nodes,
        edges=edges,
        groups=[ArchitectureGroup(group_id="route_stages", label="Route Stages")],
        inputs=route.allowed_inputs,
        outputs=route.advisor_outputs,
        mapping_notes=[
            "Route is planned and requires a real experiment before success claims.",
            "Derived from Experiment Route DSL, not from VGGT execution.",
        ],
        export_formats=[
            ArchitectureExportFormat.MERMAID,
            ArchitectureExportFormat.GRAPHVIZ,
            ArchitectureExportFormat.MARKDOWN,
        ],
        limitations=[
            "derived-from-fixture / requires-human-review",
            "not executed by TuringResearch",
            "No Modal or VGGT run was performed.",
        ],
        requires_human_review=True,
    )


def _nodes_from_items(items: list[str], prefix: str, group: str) -> list[ArchitectureNode]:
    return [
        ArchitectureNode(node_id=f"{prefix}_{index}", label=item, group=group)
        for index, item in enumerate(items, start=1)
    ]


def _chain_edges(nodes: list[ArchitectureNode], label: str) -> list[ArchitectureEdge]:
    return [
        ArchitectureEdge(source=source.node_id, target=target.node_id, label=label)
        for source, target in zip(nodes, nodes[1:], strict=False)
    ]


def _groups_for(nodes: list[ArchitectureNode]) -> list[ArchitectureGroup]:
    seen: dict[str, str] = {}
    for node in nodes:
        if node.group:
            seen[_slug(node.group)] = node.group
    return [ArchitectureGroup(group_id=group_id, label=label) for group_id, label in seen.items()]


def _slug(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_]+", "_", value.strip().lower())
    return safe.strip("_") or "node"
