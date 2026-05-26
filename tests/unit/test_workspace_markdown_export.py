from __future__ import annotations

from pathlib import Path

from turing_research_plus.workspace.markdown_export import render_workspace_overview_markdown
from turing_research_plus.workspace.project_index import ProjectIndex
from turing_research_plus.workspace.registry import load_workspace_registry

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_workspace_markdown_export_contains_projects_and_boundaries() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))
    markdown = render_workspace_overview_markdown(index.build_overview())

    assert "Workspace Overview" in markdown
    assert "vggt_human_prior" in markdown
    assert "demo_medical_imaging" in markdown
    assert "Evidence source: `false`" in markdown
    assert "Workspace index is not an evidence source" in markdown
