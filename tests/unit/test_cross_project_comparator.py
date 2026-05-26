from __future__ import annotations

from pathlib import Path

from turing_research_plus.cross_project.comparator import compare_cross_project_graph
from turing_research_plus.cross_project.evidence_graph import (
    build_cross_project_graph_from_workspace,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_cross_project_comparator_reports_reuse_hints_only() -> None:
    graph = build_cross_project_graph_from_workspace(FIXTURE)
    comparison = compare_cross_project_graph(graph)

    assert comparison.workspace_id == "demo_workspace"
    assert comparison.requires_human_review is True
    assert comparison.evidence_transfer is False
    assert comparison.shared_route_patterns
    assert comparison.shared_artifact_patterns
    assert comparison.claims_missing_evidence
    assert any("Reusable patterns are hints only" in note for note in comparison.notes)
