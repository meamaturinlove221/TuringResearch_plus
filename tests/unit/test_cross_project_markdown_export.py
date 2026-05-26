from __future__ import annotations

from pathlib import Path

from turing_research_plus.cross_project.evidence_graph import (
    build_cross_project_graph_from_workspace,
)
from turing_research_plus.cross_project.markdown_export import (
    render_cross_project_graph_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_cross_project_markdown_keeps_review_boundary() -> None:
    graph = build_cross_project_graph_from_workspace(FIXTURE)
    markdown = render_cross_project_graph_markdown(graph)

    assert "# Cross-project Evidence Graph" in markdown
    assert "Shared Methods" in markdown
    assert "Claims Missing Evidence" in markdown
    assert "not a source of evidence" in markdown
    assert "does not transfer proof" in markdown
    assert "D:/vggt" not in markdown
