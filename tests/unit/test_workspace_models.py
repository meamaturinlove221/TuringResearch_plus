from __future__ import annotations

import pytest

from turing_research_plus.workspace.models import (
    ProjectStatus,
    Workspace,
    WorkspaceOverview,
    WorkspaceProject,
)


def test_workspace_project_requires_human_review() -> None:
    with pytest.raises(ValueError, match="require human review"):
        WorkspaceProject(
            project_id="demo",
            project_name="Demo",
            project_root="demo",
            requires_human_review=False,
        )


def test_demo_only_project_must_be_fake_demo() -> None:
    with pytest.raises(ValueError, match="demo-only projects"):
        WorkspaceProject(
            project_id="demo",
            project_name="Demo",
            project_root="demo",
            status=ProjectStatus.DEMO_ONLY,
            fake_demo=False,
        )


def test_workspace_rejects_duplicate_project_ids() -> None:
    project = WorkspaceProject(
        project_id="demo",
        project_name="Demo",
        project_root="demo",
    )

    with pytest.raises(ValueError, match="unique"):
        Workspace(
            workspace_id="workspace",
            workspace_name="Workspace",
            workspace_root=".",
            projects=[project, project],
        )


def test_workspace_overview_is_not_evidence_source() -> None:
    with pytest.raises(ValueError, match="not an evidence source"):
        WorkspaceOverview(
            workspace_id="workspace",
            workspace_name="Workspace",
            project_count=0,
            evidence_source=True,
        )
