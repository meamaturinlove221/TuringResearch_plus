"""Local tool wrappers for multi-project workspaces."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.workspace.context_loader import load_workspace_context
from turing_research_plus.workspace.markdown_export import render_workspace_overview_markdown
from turing_research_plus.workspace.models import WorkspaceContext, WorkspaceOverview
from turing_research_plus.workspace.project_index import ProjectIndex
from turing_research_plus.workspace.registry import load_workspace_registry


def workspace_load(path: Path) -> ProjectIndex:
    """Load a local workspace registry and return a read-only index."""

    return ProjectIndex(load_workspace_registry(path))


def workspace_overview(path: Path) -> WorkspaceOverview:
    """Load a local workspace registry and build an overview."""

    return workspace_load(path).build_overview()


def workspace_overview_markdown(path: Path) -> str:
    """Render a local workspace overview as Markdown."""

    return render_workspace_overview_markdown(workspace_overview(path))


def workspace_project_context(path: Path, project_id: str) -> WorkspaceContext:
    """Load small local context files for one project."""

    index = workspace_load(path)
    return load_workspace_context(index.get_project(project_id))
