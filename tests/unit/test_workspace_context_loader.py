from __future__ import annotations

from pathlib import Path

from turing_research_plus.workspace.context_loader import load_workspace_context
from turing_research_plus.workspace.project_index import ProjectIndex
from turing_research_plus.workspace.registry import load_workspace_registry

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "workspaces" / "demo_workspace" / "workspace.yaml"


def test_workspace_context_loader_reads_small_local_files() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))
    context = load_workspace_context(index.get_project("demo_medical_imaging"))

    assert "north_star" in context.loaded_files
    assert "evidence_ledger" in context.loaded_files
    assert context.evidence_source is False
    assert context.requires_human_review is True
    assert "patient data" in context.loaded_files["evidence_ledger"]


def test_workspace_context_loader_marks_missing_files() -> None:
    index = ProjectIndex(load_workspace_registry(FIXTURE))
    context = load_workspace_context(
        index.get_project("vggt_human_prior"),
        relative_files=[("docs/missing.md", "missing")],
    )

    assert context.loaded_files == {}
    assert context.missing_files == ["docs/missing.md"]
