"""Safety policy for provider-neutral object artifact indexes."""

from __future__ import annotations

from pathlib import PurePosixPath

from turing_research_plus.object_store.models import ObjectArtifactStatus

ALLOWED_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".txt", ".png", ".jpg", ".jpeg"}
FORBIDDEN_NAMES = {".env"}
FORBIDDEN_PARTS = {
    ".cache",
    ".codex",
    "__pycache__",
    ".git",
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


def safety_warnings_for_object_key(
    key: str,
    *,
    size: int = 0,
    max_size: int = 2_000_000,
) -> list[str]:
    """Return object-key safety warnings without downloading payloads."""

    object_path = PurePosixPath(key.replace("\\", "/"))
    lower_name = object_path.name.lower()
    lower_parts = {part.lower() for part in object_path.parts}
    suffix = object_path.suffix.lower()
    warnings: list[str] = []
    if ".." in object_path.parts:
        warnings.append("path-traversal")
    if object_path.name in FORBIDDEN_NAMES or lower_name.endswith(".env"):
        warnings.append("forbidden-env-file")
    if lower_parts & FORBIDDEN_PARTS:
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


def status_for_object_warnings(warnings: list[str]) -> ObjectArtifactStatus:
    """Classify an object from safety warnings."""

    if not warnings:
        return ObjectArtifactStatus.SELECTED
    if any(
        warning
        in {
            "path-traversal",
            "forbidden-env-file",
            "forbidden-private-or-cache-path",
            "forbidden-secret-or-body-model-pattern",
        }
        for warning in warnings
    ):
        return ObjectArtifactStatus.UNSAFE
    if "file-too-large" in warnings or "summary-only-required" in warnings:
        return ObjectArtifactStatus.LARGE_METADATA_ONLY
    return ObjectArtifactStatus.OMITTED


def omitted_reason_for_object(warnings: list[str]) -> str:
    """Return a stable omitted reason."""

    if "path-traversal" in warnings:
        return "object key contains path traversal"
    if "forbidden-env-file" in warnings:
        return "environment files are forbidden"
    if "forbidden-private-or-cache-path" in warnings:
        return "private data, raw data, secrets, or cache keys are forbidden"
    if "forbidden-secret-or-body-model-pattern" in warnings:
        return "secret or SMPL-X body model pattern is forbidden"
    if "summary-only-required" in warnings:
        return "npz, pkl, or body-model-like object requires metadata-only import"
    if "file-too-large" in warnings:
        return "object exceeds max selected size"
    if "unsupported-file-type" in warnings:
        return "object type is not in the artifact allow-list"
    return "object omitted by safety policy"
