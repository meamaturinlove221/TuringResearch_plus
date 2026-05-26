"""Manifest helpers for dry-run repository split exports."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from turing_research_plus.repo_split.models import RepoSplitManifest


def sha256_file(path: Path) -> str:
    """Return a SHA256 digest for a file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def split_manifest_to_yaml(manifest: RepoSplitManifest) -> str:
    """Render a simple YAML manifest without requiring a YAML dependency."""

    return _to_yaml(manifest.model_dump(mode="json"))


def _to_yaml(value: Any, indent: int = 0) -> str:
    spaces = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, item in value.items():
            if isinstance(item, dict | list):
                lines.append(f"{spaces}{key}:")
                lines.append(_to_yaml(item, indent + 2).rstrip())
            else:
                lines.append(f"{spaces}{key}: {_scalar(item)}")
        return "\n".join(lines) + "\n"
    if isinstance(value, list):
        if not value:
            return f"{spaces}[]\n"
        lines = []
        for item in value:
            if isinstance(item, dict):
                lines.append(f"{spaces}-")
                lines.append(_to_yaml(item, indent + 2).rstrip())
            else:
                lines.append(f"{spaces}- {_scalar(item)}")
        return "\n".join(lines) + "\n"
    if isinstance(value, BaseModel):
        return _to_yaml(value.model_dump(mode="json"), indent)
    return f"{spaces}{_scalar(value)}\n"


def _scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    text = str(value)
    if not text:
        return '""'
    if any(char in text for char in [":", "#", "{", "}", "[", "]", ","]) or text != text.strip():
        return '"' + text.replace('"', '\\"') + '"'
    return text
