"""Load small local workspace context files."""

from __future__ import annotations

from turing_research_plus.workspace.models import WorkspaceContext, WorkspaceProject

DEFAULT_CONTEXT_FILES = [
    ("docs/north_star.md", "north_star"),
    ("docs/evidence_ledger.md", "evidence_ledger"),
    ("docs/artifact_plan.md", "artifact_plan"),
    ("docs/experiment_routes.md", "experiment_routes"),
    ("docs/related_work.md", "related_work"),
    ("docs/advisor_pack.md", "advisor_pack"),
]


def load_workspace_context(
    project: WorkspaceProject,
    *,
    relative_files: list[tuple[str, str]] | None = None,
    max_bytes: int = 100_000,
) -> WorkspaceContext:
    """Load small local Markdown context files for a workspace project."""

    loaded: dict[str, str] = {}
    missing: list[str] = []
    warnings: list[str] = []
    for relative_path, label in relative_files or DEFAULT_CONTEXT_FILES:
        path = project.project_root / relative_path
        if not path.exists() or not path.is_file():
            missing.append(relative_path)
            continue
        size = path.stat().st_size
        if size > max_bytes:
            missing.append(relative_path)
            warnings.append(f"{relative_path}: file too large for context loader")
            continue
        loaded[label] = path.read_text(encoding="utf-8")

    return WorkspaceContext(
        project_id=project.project_id,
        loaded_files=loaded,
        missing_files=missing,
        safety_warnings=warnings,
        requires_human_review=True,
        evidence_source=False,
    )
