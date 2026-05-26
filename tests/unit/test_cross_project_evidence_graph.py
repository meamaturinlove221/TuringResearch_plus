from __future__ import annotations

from pathlib import Path

from turing_research_plus.cross_project.evidence_graph import (
    build_cross_project_graph_from_workspace,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_build_cross_project_graph_from_demo_workspace() -> None:
    graph = build_cross_project_graph_from_workspace(FIXTURE)

    assert graph.workspace_id == "demo_workspace"
    assert len(graph.project_nodes) == 2
    assert graph.requires_human_review is True
    assert graph.evidence_source is False
    assert graph.shared_failures
    assert graph.reusable_templates
    assert graph.missing_evidence_claims
    assert all(edge.evidence_transfer is False for edge in graph.cross_project_edges)
    assert "vggt_human_prior" in {node.project_id for node in graph.method_nodes}
    assert "demo_medical_imaging" in {node.project_id for node in graph.method_nodes}


def test_cross_project_graph_serializes_to_json_safe_refs() -> None:
    graph = build_cross_project_graph_from_workspace(FIXTURE)
    payload = graph.model_dump(mode="json")
    rendered = str(payload)

    assert payload["requires_human_review"] is True
    assert "workspace://vggt_human_prior" in rendered
    assert "D:/vggt" not in rendered
