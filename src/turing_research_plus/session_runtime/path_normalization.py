"""Cross-platform archive path normalization for session runtime packages."""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field

WINDOWS_DRIVE_PATTERN = re.compile(r"^[A-Za-z]:/")


class NormalizedArchivePath(BaseModel):
    """Safety decision for one archive member path."""

    model_config = ConfigDict(extra="forbid")

    original_path: str = Field(min_length=1)
    normalized_path: str = Field(min_length=1)
    blocked_reasons: list[str] = Field(default_factory=list)

    @property
    def release_blocker(self) -> bool:
        """Return whether this path is unsafe for archive use."""

        return bool(self.blocked_reasons)

    @property
    def safe(self) -> bool:
        """Return whether this path is safe for archive use."""

        return not self.release_blocker


def windows_path_to_posix(path: str) -> str:
    """Convert Windows separators to POSIX separators without marking safety."""

    return path.replace("\\", "/")


def normalize_archive_member_path(path: str) -> NormalizedArchivePath:
    """Normalize an archive member path and report unsafe path patterns."""

    raw = windows_path_to_posix(path.strip())
    reasons: list[str] = []

    if not raw:
        reasons.append("empty-archive-path")
        raw = "."
    if raw.startswith("//"):
        reasons.append("unc-or-network-path")
    if raw.startswith("/"):
        reasons.append("absolute-path")
    if WINDOWS_DRIVE_PATTERN.match(raw):
        reasons.append("windows-drive-path")

    parts = [part for part in raw.split("/") if part not in {"", "."}]
    if any(part == ".." for part in parts):
        reasons.append("path-traversal")
    if not parts:
        reasons.append("empty-archive-path")

    normalized = PurePosixPath(*[part for part in parts if part != ".."]).as_posix()
    if normalized == ".":
        normalized = raw

    return NormalizedArchivePath(
        original_path=path,
        normalized_path=normalized,
        blocked_reasons=list(dict.fromkeys(reasons)),
    )


def require_safe_archive_member_path(path: str) -> str:
    """Return a normalized path or raise if the archive member path is unsafe."""

    report = normalize_archive_member_path(path)
    if report.release_blocker:
        reasons = ", ".join(report.blocked_reasons)
        raise ValueError(f"unsafe archive member path: {reasons}")
    return report.normalized_path
