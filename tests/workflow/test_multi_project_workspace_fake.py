from __future__ import annotations

from pathlib import Path

from turing_research_plus.workspace.tools import (
    workspace_overview,
    workspace_overview_markdown,
    workspace_project_context,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_multi_project_workspace_fake_demo_keeps_project_boundaries() -> None:
    overview = workspace_overview(FIXTURE)
    markdown = workspace_overview_markdown(FIXTURE)
    vggt_context = workspace_project_context(FIXTURE, "vggt_human_prior")
    medical_context = workspace_project_context(FIXTURE, "demo_medical_imaging")

    assert overview.project_count == 2
    assert overview.evidence_source is False
    assert all(project.requires_human_review for project in overview.projects)
    assert any(project.project_id == "vggt_human_prior" for project in overview.projects)
    assert any(project.project_id == "demo_medical_imaging" for project in overview.projects)
    assert "SparseConv3D success is not established" in vggt_context.loaded_files["evidence_ledger"]
    assert "No real patient data" in medical_context.loaded_files["evidence_ledger"]
    assert "Workspace index is not an evidence source" in markdown
    assert "D:/vggt" not in markdown
