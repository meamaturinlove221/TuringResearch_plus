"""Safety policy for GitHub artifact sync."""

from __future__ import annotations

from pathlib import PurePosixPath

ALLOWED_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".txt", ".png", ".jpg", ".jpeg"}
FORBIDDEN_NAMES = {".env"}
FORBIDDEN_PARTS = {
    ".cache",
    ".codex",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "private_data",
    "raw_data",
    "raw_dataset",
    "datasets",
    "secrets",
}
FORBIDDEN_PATTERNS = (
    "apikey",
    "api_key",
    "api-key",
    "token",
    "secret",
    "smplx_",
    "smpl-x",
)


def safety_warnings_for_artifact_path(
    path: str,
    *,
    size: int = 0,
    max_size: int = 2_000_000,
) -> list[str]:
    """Return warnings for a GitHub artifact path."""

    artifact_path = PurePosixPath(path.replace("\\", "/"))
    lower_name = artifact_path.name.lower()
    parts = {part.lower() for part in artifact_path.parts}
    suffix = artifact_path.suffix.lower()
    warnings: list[str] = []
    if artifact_path.name in FORBIDDEN_NAMES or lower_name.endswith(".env"):
        warnings.append("forbidden-env-file")
    if parts & FORBIDDEN_PARTS:
        warnings.append("forbidden-private-or-cache-path")
    if any(pattern in lower_name for pattern in FORBIDDEN_PATTERNS):
        warnings.append("forbidden-secret-or-body-model-pattern")
    if suffix in {".npz", ".pkl"}:
        warnings.append("summary-only-required")
    if suffix and suffix not in ALLOWED_SUFFIXES:
        warnings.append("unsupported-file-type")
    if size > max_size:
        warnings.append("file-too-large")
    return list(dict.fromkeys(warnings))


def should_select_artifact(path: str, *, size: int = 0, max_size: int = 2_000_000) -> bool:
    """Return whether a GitHub artifact should be selected by default."""

    return safety_warnings_for_artifact_path(path, size=size, max_size=max_size) == []


def omitted_reason_for_artifact(warnings: list[str]) -> str:
    """Return a stable omitted reason."""

    if "summary-only-required" in warnings:
        return "npz, pkl, or body-model-like file requires summary-only import"
    if "file-too-large" in warnings:
        return "artifact exceeds max selected file size"
    if "forbidden-env-file" in warnings:
        return "environment files are forbidden"
    if "forbidden-private-or-cache-path" in warnings:
        return "private data, secrets, raw data, or cache paths are forbidden"
    if "forbidden-secret-or-body-model-pattern" in warnings:
        return "secret or SMPL-X body model pattern is forbidden"
    if "unsupported-file-type" in warnings:
        return "file type is not in the GitHub artifact allow-list"
    return "artifact omitted by safety policy"
