"""Safety rules for handoff bundles."""

from __future__ import annotations

from pathlib import Path

ALLOWED_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".png", ".jpg", ".jpeg", ".txt"}
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
FORBIDDEN_PATTERNS = ("apikey", "api_key", "api-key", "token", "secret", "SMPLX_", "SMPL-X")


def safety_warnings_for_path(
    path: Path,
    *,
    file_size: int | None = None,
    max_size: int = 2_000_000,
) -> list[str]:
    """Return safety warnings for a candidate handoff file."""

    warnings: list[str] = []
    name = path.name
    suffix = path.suffix.lower()
    parts = {part.lower() for part in path.parts}
    lower_name = name.lower()
    if name in FORBIDDEN_NAMES or lower_name.endswith(".env"):
        warnings.append("forbidden-env-file")
    if parts & FORBIDDEN_PARTS:
        warnings.append("forbidden-private-or-cache-path")
    if any(pattern.lower() in lower_name for pattern in FORBIDDEN_PATTERNS):
        warnings.append("forbidden-secret-or-body-model-pattern")
    if suffix in {".npz", ".pkl"}:
        warnings.append("summary-only-required")
    if suffix and suffix not in ALLOWED_SUFFIXES:
        warnings.append("unsupported-file-type")
    if file_size is not None and file_size > max_size:
        warnings.append("file-too-large")
    return list(dict.fromkeys(warnings))


def should_include_file(
    path: Path,
    *,
    file_size: int | None = None,
    max_size: int = 2_000_000,
) -> bool:
    """Return whether a file is safe to include."""

    return safety_warnings_for_path(path, file_size=file_size, max_size=max_size) == []


def omitted_reason(path: Path, warnings: list[str]) -> str:
    """Build a human-readable omitted reason."""

    if "summary-only-required" in warnings:
        return "npz or body-model-like file requires summary-only handoff"
    if "file-too-large" in warnings:
        return "file exceeds handoff max size"
    if "forbidden-env-file" in warnings:
        return "environment files are forbidden"
    if "forbidden-private-or-cache-path" in warnings:
        return "private data, secrets, or cache paths are forbidden"
    if "forbidden-secret-or-body-model-pattern" in warnings:
        return "secret or SMPL-X body model pattern is forbidden"
    if "unsupported-file-type" in warnings:
        return "file type is not in the handoff allow-list"
    return "file omitted by handoff safety policy"
