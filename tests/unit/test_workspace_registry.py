from __future__ import annotations

from pathlib import Path

from turing_research_plus.workspace.registry import load_workspace_registry

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_load_workspace_registry_reads_demo_workspace() -> None:
    workspace = load_workspace_registry(FIXTURE)

    assert workspace.workspace_id == "demo_workspace"
    assert len(workspace.projects) == 2
    assert {project.project_id for project in workspace.projects} == {
        "vggt_human_prior",
        "demo_medical_imaging",
    }
    assert all(project.requires_human_review for project in workspace.projects)
    assert all(not project.human_verified for project in workspace.projects)


def test_workspace_registry_resolves_relative_paths() -> None:
    workspace = load_workspace_registry(FIXTURE)
    vggt = next(
        project for project in workspace.projects if project.project_id == "vggt_human_prior"
    )

    assert vggt.project_root.is_absolute()
    assert vggt.docs_path is not None
    assert vggt.docs_path.name == "docs"
    assert vggt.evidence_path is not None
    assert vggt.evidence_path.name == "evidence_ledger.md"
