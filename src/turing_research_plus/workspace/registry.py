"""Load multi-project workspace registries from local files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.workspace.models import Workspace, WorkspaceProject


def load_workspace_registry(path: Path) -> Workspace:
    """Load a workspace registry from a local JSON or simple YAML file."""

    payload = _load_mapping(path)
    workspace_root = _resolve_workspace_root(path, payload.get("workspace_root"))
    projects = [
        _project_from_payload(project_payload, workspace_root)
        for project_payload in payload.get("projects", [])
    ]
    return Workspace(
        workspace_id=payload["workspace_id"],
        workspace_name=payload.get("workspace_name", payload["workspace_id"]),
        workspace_root=workspace_root,
        projects=projects,
        status=payload.get("status", "active"),
        privacy_level=payload.get("privacy_level", "internal"),
        requires_human_review=payload.get("requires_human_review", True),
        limitations=payload.get("limitations", []),
    )


def _load_mapping(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        data = _parse_simple_workspace_yaml(text)
    if not isinstance(data, dict):
        raise ValueError("workspace registry must contain a mapping")
    return data


def _resolve_workspace_root(path: Path, configured_root: object | None) -> Path:
    if configured_root is None:
        return path.parent.resolve()
    root = Path(str(configured_root))
    if root.is_absolute():
        return root
    return (path.parent / root).resolve()


def _project_from_payload(payload: dict[str, Any], workspace_root: Path) -> WorkspaceProject:
    project_root = _resolve_project_path(workspace_root, payload["project_root"])
    return WorkspaceProject(
        project_id=payload["project_id"],
        project_name=payload.get("project_name", payload["project_id"]),
        project_type=payload.get("project_type", "unknown"),
        project_root=project_root,
        docs_path=_optional_project_path(project_root, payload.get("docs_path")),
        evidence_path=_optional_project_path(project_root, payload.get("evidence_path")),
        artifacts_path=_optional_project_path(project_root, payload.get("artifacts_path")),
        advisor_pack_path=_optional_project_path(project_root, payload.get("advisor_pack_path")),
        routes_path=_optional_project_path(project_root, payload.get("routes_path")),
        status=payload.get("status", "unknown"),
        privacy_level=payload.get("privacy_level", "internal"),
        tags=list(payload.get("tags", [])),
        notes=list(payload.get("notes", [])),
        requires_human_review=payload.get("requires_human_review", True),
        fake_demo=payload.get("fake_demo", False),
    )


def _resolve_project_path(workspace_root: Path, value: object) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return (workspace_root / path).resolve()


def _optional_project_path(project_root: Path, value: object | None) -> Path | None:
    if value is None:
        return None
    path = Path(str(value))
    if path.is_absolute():
        return path
    return (project_root / path).resolve()


def _parse_simple_workspace_yaml(text: str) -> dict[str, Any]:
    """Parse the small YAML subset used by workspace fixtures.

    This intentionally avoids adding a runtime dependency. It supports top-level
    scalar fields, top-level string lists, and a `projects` list of mappings.
    """

    result: dict[str, Any] = {}
    current_list_key: str | None = None
    current_project: dict[str, Any] | None = None
    current_project_list_key: str | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0 and line.endswith(":"):
            key = line[:-1]
            if key == "projects":
                result[key] = []
                current_list_key = "projects"
            else:
                result[key] = []
                current_list_key = key
            current_project = None
            current_project_list_key = None
            continue

        if indent == 0 and ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = _parse_scalar(value.strip())
            current_list_key = None
            current_project = None
            current_project_list_key = None
            continue

        if indent == 2 and line.startswith("- ") and current_list_key == "projects":
            projects = result.setdefault("projects", [])
            current_project = {}
            projects.append(current_project)
            current_project_list_key = None
            remainder = line[2:].strip()
            if remainder:
                key, value = remainder.split(":", 1)
                current_project[key.strip()] = _parse_scalar(value.strip())
            continue

        if indent == 2 and line.startswith("- ") and current_list_key:
            result[current_list_key].append(_parse_scalar(line[2:].strip()))
            continue

        if indent == 4 and current_project is not None and line.endswith(":"):
            key = line[:-1]
            current_project[key] = []
            current_project_list_key = key
            continue

        if indent == 4 and current_project is not None and ":" in line:
            key, value = line.split(":", 1)
            current_project[key.strip()] = _parse_scalar(value.strip())
            current_project_list_key = None
            continue

        if indent == 6 and current_project is not None and current_project_list_key:
            if line.startswith("- "):
                current_project[current_project_list_key].append(_parse_scalar(line[2:].strip()))
            continue

        raise ValueError(f"unsupported workspace YAML line: {raw_line!r}")

    return result


def _parse_scalar(value: str) -> object:
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "None"}:
        return None
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value
