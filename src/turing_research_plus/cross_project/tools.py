"""Local tool wrappers for cross-project evidence graph helpers."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.cross_project.comparator import compare_cross_project_graph
from turing_research_plus.cross_project.evidence_graph import (
    build_cross_project_graph_from_workspace,
)
from turing_research_plus.cross_project.markdown_export import (
    render_cross_project_graph_markdown,
)
from turing_research_plus.cross_project.models import (
    CrossProjectComparison,
    CrossProjectEvidenceGraph,
)


def workspace_cross_project_graph(path: Path) -> CrossProjectEvidenceGraph:
    """Build a local cross-project graph from a workspace registry."""

    return build_cross_project_graph_from_workspace(path)


def workspace_cross_project_compare(path: Path) -> CrossProjectComparison:
    """Build a cross-project comparison from a workspace registry."""

    return compare_cross_project_graph(workspace_cross_project_graph(path))


def workspace_cross_project_markdown(path: Path) -> str:
    """Render a cross-project graph from a workspace registry as Markdown."""

    return render_cross_project_graph_markdown(workspace_cross_project_graph(path))
