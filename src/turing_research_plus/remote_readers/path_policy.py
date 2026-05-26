"""Remote path policy for read-only artifact inspection."""

from __future__ import annotations

from pathlib import PurePosixPath

FORBIDDEN_ROOTS = {
    "/",
    "/etc",
    "/home",
    "/root",
    "/var",
    "/usr",
    "/opt",
    "~",
}

FORBIDDEN_PARTS = {
    ".cache",
    ".codex",
    ".git",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "private_data",
    "raw_data",
    "raw_dataset",
    "datasets",
    "secrets",
}


def normalize_remote_path(path: str) -> str:
    """Normalize a remote path to a conservative POSIX form."""

    cleaned = path.replace("\\", "/").strip()
    while "//" in cleaned:
        cleaned = cleaned.replace("//", "/")
    return cleaned.rstrip("/") or "."


def path_policy_warnings(path: str, *, root_path: str | None = None) -> list[str]:
    """Return path policy warnings without touching a remote host."""

    normalized = normalize_remote_path(path)
    posix_path = PurePosixPath(normalized)
    lower_parts = {part.lower() for part in posix_path.parts}
    warnings: list[str] = []

    if ".." in posix_path.parts:
        warnings.append("path-traversal")
    if normalized in FORBIDDEN_ROOTS:
        warnings.append("forbidden-root-path")
    if lower_parts & FORBIDDEN_PARTS:
        warnings.append("forbidden-private-or-cache-path")
    if root_path:
        normalized_root = normalize_remote_path(root_path)
        if normalized_root not in {".", "/"} and not normalized.startswith(normalized_root):
            warnings.append("outside-configured-root")
    return list(dict.fromkeys(warnings))


def remote_path_is_allowed(path: str, *, root_path: str | None = None) -> bool:
    """Return whether the remote path passes policy checks."""

    return path_policy_warnings(path, root_path=root_path) == []
