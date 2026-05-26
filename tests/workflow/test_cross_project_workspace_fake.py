from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.cross_project.tools import (
    workspace_cross_project_graph,
    workspace_cross_project_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"
GRAPH_JSON = ROOT / "examples" / "workspaces" / "demo_workspace" / "cross_project_graph.json"
SUMMARY_MD = ROOT / "examples" / "workspaces" / "demo_workspace" / "cross_project_summary.md"


def test_cross_project_workspace_fake_outputs_are_review_only() -> None:
    graph = workspace_cross_project_graph(FIXTURE)
    markdown = workspace_cross_project_markdown(FIXTURE)
    fixture_payload = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    fixture_markdown = SUMMARY_MD.read_text(encoding="utf-8")

    assert graph.requires_human_review is True
    assert graph.evidence_source is False
    assert len(graph.project_nodes) == 2
    assert graph.shared_failures
    assert all(edge.evidence_transfer is False for edge in graph.cross_project_edges)
    assert "not a source of evidence" in markdown
    assert fixture_payload["workspace_id"] == "demo_workspace"
    assert fixture_payload["requires_human_review"] is True
    assert "does not transfer proof" in fixture_markdown
    assert "SparseConv3D success" not in fixture_markdown
    assert "D:/vggt" not in fixture_markdown
