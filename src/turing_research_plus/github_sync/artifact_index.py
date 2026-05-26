"""Local artifact index parsing and normalization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.github_sync.models import (
    GitHubArtifactRecord,
    GitHubArtifactSourceType,
)


def load_artifact_index(path: Path) -> list[GitHubArtifactRecord]:
    """Load a JSON artifact index fixture."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        artifacts = payload.get("artifacts", [])
    else:
        artifacts = payload
    if not isinstance(artifacts, list):
        raise ValueError("artifact index must contain a list of artifacts")
    return [_record_from_mapping(item) for item in artifacts if isinstance(item, dict)]


def _record_from_mapping(item: dict[str, Any]) -> GitHubArtifactRecord:
    source_type_raw = item.get("source_type", GitHubArtifactSourceType.MANUAL_INDEX.value)
    return GitHubArtifactRecord(
        name=str(item.get("name") or item.get("path") or "artifact"),
        path=str(item.get("path") or item.get("name") or "artifact"),
        source_type=GitHubArtifactSourceType(str(source_type_raw)),
        size=int(item.get("size") or item.get("file_size") or 0),
        sha256=item.get("sha256"),
        download_url=item.get("download_url"),
        content_type=item.get("content_type"),
        metadata={str(key): str(value) for key, value in dict(item.get("metadata", {})).items()},
    )


def filter_selected_artifacts(
    artifacts: list[GitHubArtifactRecord],
    selected_patterns: list[str],
) -> list[GitHubArtifactRecord]:
    """Select artifacts by substring patterns, or return all when no pattern is set."""

    if not selected_patterns:
        return artifacts
    lowered_patterns = [pattern.lower() for pattern in selected_patterns]
    return [
        artifact
        for artifact in artifacts
        if any(pattern in artifact.path.lower() for pattern in lowered_patterns)
    ]
