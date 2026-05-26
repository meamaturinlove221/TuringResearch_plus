"""Project index helpers for multi-project workspaces."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.workspace.models import (
    Workspace,
    WorkspaceOverview,
    WorkspaceProject,
    WorkspaceProjectSummary,
)


class ProjectIndex:
    """Read-only project index for a workspace registry."""

    def __init__(self, workspace: Workspace) -> None:
        self.workspace = workspace
        self._projects = {project.project_id: project for project in workspace.projects}

    def list_projects(self) -> list[WorkspaceProject]:
        """Return indexed projects in registry order."""

        return list(self.workspace.projects)

    def get_project(self, project_id: str) -> WorkspaceProject:
        """Return one project by id."""

        try:
            return self._projects[project_id]
        except KeyError as exc:
            raise KeyError(f"workspace project not found: {project_id}") from exc

    def summarize_project_state(self, project_id: str) -> WorkspaceProjectSummary:
        """Summarize paths and review status for one project."""

        project = self.get_project(project_id)
        path_map = _project_paths(project)
        existing_paths = [
            label for label, path in path_map.items() if path is not None and path.exists()
        ]
        missing_paths = [
            label for label, path in path_map.items() if path is None or not path.exists()
        ]
        return WorkspaceProjectSummary(
            project_id=project.project_id,
            project_name=project.project_name,
            project_type=project.project_type,
            status=project.status,
            privacy_level=project.privacy_level,
            existing_paths=existing_paths,
            missing_paths=missing_paths,
            notes=project.notes,
            requires_human_review=True,
            fake_demo=project.fake_demo,
            evidence_source=False,
        )

    def build_overview(self) -> WorkspaceOverview:
        """Build a read-only workspace overview."""

        summaries = [
            self.summarize_project_state(project.project_id)
            for project in self.workspace.projects
        ]
        missing_paths = {
            summary.project_id: summary.missing_paths
            for summary in summaries
            if summary.missing_paths
        }
        warnings = []
        if any(summary.privacy_level.value != "public-demo" for summary in summaries):
            warnings.append("workspace contains non-public-demo projects")
        return WorkspaceOverview(
            workspace_id=self.workspace.workspace_id,
            workspace_name=self.workspace.workspace_name,
            project_count=len(summaries),
            projects=summaries,
            missing_paths=missing_paths,
            safety_warnings=warnings,
            limitations=[
                "Workspace index is not an evidence source.",
                "No automatic data ingestion is performed.",
                "Project evidence remains scoped to its own project.",
            ],
            requires_human_review=True,
            evidence_source=False,
        )


def _project_paths(project: WorkspaceProject) -> dict[str, Path | None]:
    return {
        "project_root": project.project_root,
        "docs_path": project.docs_path,
        "evidence_path": project.evidence_path,
        "artifacts_path": project.artifacts_path,
        "advisor_pack_path": project.advisor_pack_path,
        "routes_path": project.routes_path,
    }
