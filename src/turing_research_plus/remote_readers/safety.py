"""Safety policy for read-only remote artifact reading."""

from __future__ import annotations

from pathlib import PurePosixPath

from turing_research_plus.remote_readers.path_policy import path_policy_warnings

ALLOWED_SUFFIXES = {".md", ".json", ".yaml", ".yml", ".csv", ".txt", ".png", ".jpg", ".jpeg"}
FORBIDDEN_NAMES = {".env"}
FORBIDDEN_PATTERNS = (
    "apikey",
    "api_key",
    "api-key",
    "token",
    "secret",
    "smplx_",
    "smpl-x",
)


def safety_warnings_for_remote_path(
    path: str,
    *,
    root_path: str | None = None,
    size: int = 0,
    max_size: int = 2_000_000,
    is_symlink: bool = False,
) -> list[str]:
    """Return warnings for a remote artifact path."""

    artifact_path = PurePosixPath(path.replace("\\", "/"))
    lower_name = artifact_path.name.lower()
    suffix = artifact_path.suffix.lower()
    warnings = path_policy_warnings(path, root_path=root_path)

    if is_symlink:
        warnings.append("symlink-requires-review")
    if artifact_path.name in FORBIDDEN_NAMES or lower_name.endswith(".env"):
        warnings.append("forbidden-env-file")
    if any(pattern in lower_name for pattern in FORBIDDEN_PATTERNS):
        warnings.append("forbidden-secret-or-body-model-pattern")
    if suffix in {".npz", ".pkl"}:
        warnings.append("summary-only-required")
    if suffix and suffix not in ALLOWED_SUFFIXES:
        warnings.append("unsupported-file-type")
    if size > max_size:
        warnings.append("file-too-large")
    return list(dict.fromkeys(warnings))


def should_select_remote_file(
    path: str,
    *,
    root_path: str | None = None,
    size: int = 0,
    max_size: int = 2_000_000,
    is_symlink: bool = False,
) -> bool:
    """Return whether a remote file should be selected by default."""

    return (
        safety_warnings_for_remote_path(
            path,
            root_path=root_path,
            size=size,
            max_size=max_size,
            is_symlink=is_symlink,
        )
        == []
    )


def omitted_reason_for_remote_file(warnings: list[str]) -> str:
    """Return a stable omitted reason."""

    if "path-traversal" in warnings or "outside-configured-root" in warnings:
        return "remote path violates configured root policy"
    if "forbidden-root-path" in warnings:
        return "remote root path is too broad to inspect"
    if "symlink-requires-review" in warnings:
        return "remote symlink requires manual review"
    if "summary-only-required" in warnings:
        return "npz, pkl, or body-model-like file requires summary-only import"
    if "file-too-large" in warnings:
        return "remote file exceeds max selected size"
    if "forbidden-env-file" in warnings:
        return "environment files are forbidden"
    if "forbidden-private-or-cache-path" in warnings:
        return "private data, raw data, secrets, or cache paths are forbidden"
    if "forbidden-secret-or-body-model-pattern" in warnings:
        return "secret or SMPL-X body model pattern is forbidden"
    if "unsupported-file-type" in warnings:
        return "file type is not in the remote reader allow-list"
    return "remote artifact omitted by safety policy"
