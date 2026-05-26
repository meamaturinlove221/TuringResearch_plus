"""Safety checks for Git-based context handoff."""

from __future__ import annotations

import re
from pathlib import Path

SECRET_VALUE_PATTERN = re.compile(
    r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{8,}"
)
FORBIDDEN_TEXT_MARKERS = (
    ".env",
    "SMPLX_",
    "SMPL-X body model",
    "private_data",
    "raw_data",
    "raw dataset",
)
FORBIDDEN_PATH_PARTS = {
    ".env",
    ".codex",
    ".cache",
    "private_data",
    "raw_data",
    "raw_dataset",
    "datasets",
    "secrets",
}


def safety_warnings_for_text(text: str) -> list[str]:
    """Return warnings for unsafe context text."""

    warnings: list[str] = []
    if SECRET_VALUE_PATTERN.search(text):
        warnings.append("possible-secret-value")
    lower = text.lower()
    for marker in FORBIDDEN_TEXT_MARKERS:
        if marker.lower() in lower:
            warnings.append(f"forbidden-marker:{marker}")
    return list(dict.fromkeys(warnings))


def safety_warnings_for_path(path: Path) -> list[str]:
    """Return warnings for unsafe context source paths."""

    warnings: list[str] = []
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    if parts & FORBIDDEN_PATH_PARTS:
        warnings.append("forbidden-private-or-secret-path")
    if any(marker.lower() in name for marker in ("apikey", "api_key", "token", "secret")):
        warnings.append("forbidden-secret-like-name")
    if name.startswith("smplx_") or "smpl-x" in name:
        warnings.append("forbidden-body-model-like-name")
    return list(dict.fromkeys(warnings))


def is_text_handoff_safe(text: str) -> bool:
    """Return whether context text is safe enough for handoff."""

    return safety_warnings_for_text(text) == []
