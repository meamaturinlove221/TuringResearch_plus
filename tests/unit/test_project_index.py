from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.workspace.project_index import ProjectIndex
from turing_research_plus.workspace.registry import load_workspace_registry

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_project_index_lists_and_gets_projects() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))

    assert [project.project_id for project in index.list_projects()] == [
        "vggt_human_prior",
        "demo_medical_imaging",
    ]
    assert index.get_project("demo_medical_imaging").fake_demo is True


def test_project_index_missing_project_raises() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))

    with pytest.raises(KeyError, match="not found"):
        index.get_project("missing")


def test_project_index_summarizes_project_state() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))
    summary = index.summarize_project_state("vggt_human_prior")

    assert summary.project_id == "vggt_human_prior"
    assert "project_root" in summary.existing_paths
    assert "evidence_path" in summary.existing_paths
    assert summary.requires_human_review is True
    assert summary.evidence_source is False


def test_project_index_builds_overview() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))
    overview = index.build_overview()

    assert overview.project_count == 2
    assert overview.evidence_source is False
    assert overview.requires_human_review is True
