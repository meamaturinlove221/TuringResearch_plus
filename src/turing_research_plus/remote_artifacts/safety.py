"""Unified remote artifact safety policy."""

from __future__ import annotations

from pathlib import PurePosixPath

from turing_research_plus.remote_artifacts.models import RemoteArtifactStatus

UNSAFE_WARNINGS = {
    "forbidden-env-file",
    "forbidden-private-or-cache-path",
    "forbidden-secret-or-body-model-pattern",
    "path-traversal",
    "symlink-requires-review",
}
METADATA_WARNINGS = {"file-too-large", "summary-only-required"}


def unified_status_from_warnings(warnings: list[str]) -> RemoteArtifactStatus:
    """Map source-specific safety warnings to a unified status."""

    warning_set = set(warnings)
    if warning_set & UNSAFE_WARNINGS:
        return RemoteArtifactStatus.UNSAFE
    if warning_set & METADATA_WARNINGS:
        return RemoteArtifactStatus.METADATA_ONLY
    if warnings:
        return RemoteArtifactStatus.OMITTED
    return RemoteArtifactStatus.SELECTED


def stable_artifact_id(source_id: str, path: str) -> str:
    """Return a stable readable artifact identifier."""

    normalized = str(PurePosixPath(path.replace("\\", "/")))
    slug = normalized.strip("/").replace("/", "__").replace(" ", "_")
    return f"{source_id}:{slug}"


def duplicate_key(path: str, sha256: str | None) -> str:
    """Return a duplicate comparison key."""

    if sha256:
        return f"sha256:{sha256}"
    normalized = path.replace("\\", "/")
    return f"path:{PurePosixPath(normalized).name.lower()}"
