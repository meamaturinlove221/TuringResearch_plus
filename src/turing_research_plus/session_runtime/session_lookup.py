"""Local session path lookup helpers."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.models import (
    SessionLookupRecord,
    SessionPreflightRequest,
)

TEXT_CONTEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".txt"}


def resolve_under_project(project_root: Path, candidate: Path) -> Path:
    """Resolve a path relative to the project root when needed."""

    if candidate.is_absolute():
        return candidate.resolve()
    return (project_root / candidate).resolve()


def discover_context_files(context_source: Path) -> list[str]:
    """Discover context files without reading private payloads."""

    source = context_source.resolve()
    if not source.exists():
        return []
    if source.is_file():
        return [source.name]

    files: list[str] = []
    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_CONTEXT_SUFFIXES and path.name != ".gitkeep":
            continue
        files.append(path.relative_to(source).as_posix())
    return files


def build_session_lookup_record(request: SessionPreflightRequest) -> SessionLookupRecord:
    """Build a stable lookup record for a preflight request."""

    project_root = request.project_root.resolve()
    context_source = resolve_under_project(project_root, request.context_source)
    output_dir = resolve_under_project(project_root, request.output_dir)
    context_files = request.candidate_paths or discover_context_files(context_source)

    return SessionLookupRecord(
        session_id=request.session_id,
        project_root=project_root.as_posix(),
        context_source=context_source.as_posix(),
        output_dir=output_dir.as_posix(),
        context_files=context_files,
    )
