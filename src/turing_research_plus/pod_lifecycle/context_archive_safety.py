"""Archive path safety checks for pod context packages."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.pod_lifecycle.transfer_policy import transfer_warnings_for_path


class ContextArchiveEntryCheck(BaseModel):
    """Safety result for one archive entry."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    normalized_path: str = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)

    @property
    def safe(self) -> bool:
        """Return whether the entry is safe to include."""

        return not self.warnings


class ContextArchiveSafetyReport(BaseModel):
    """Safety report for archive entries."""

    model_config = ConfigDict(extra="forbid")

    entries: list[ContextArchiveEntryCheck] = Field(default_factory=list)
    dotfile_policy: str = "forbidden dotfiles are excluded unless generated and explicit"
    path_policy: str = "relative POSIX paths only; no absolute paths or traversal"
    shell_policy: str = "shell metacharacters are flagged before packaging"
    windows_linux_compatibility_notes: list[str] = Field(
        default_factory=lambda: [
            "Normalize archive entries to forward-slash relative paths.",
            "Validate entries before unpacking on Linux or Windows.",
            "Do not trust platform-specific absolute paths inside archives.",
        ]
    )

    @property
    def release_blocker(self) -> bool:
        """Return whether any archive entry is unsafe."""

        return any(not entry.safe for entry in self.entries)

    @property
    def blocked_paths(self) -> list[str]:
        """Return unsafe archive entry paths."""

        return [entry.path for entry in self.entries if not entry.safe]


def normalize_archive_entry(path: str) -> str:
    """Normalize an archive entry to a POSIX-like relative path string."""

    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def validate_archive_entry(path: str, *, file_size: int | None = None) -> ContextArchiveEntryCheck:
    """Validate one context archive entry without touching the filesystem."""

    normalized = normalize_archive_entry(path)
    warnings = transfer_warnings_for_path(normalized, file_size=file_size)
    if PurePosixPath(normalized).is_absolute():
        warnings.append("unsafe-archive-absolute-path")
    return ContextArchiveEntryCheck(
        path=path,
        normalized_path=normalized or ".",
        warnings=list(dict.fromkeys(warnings)),
    )


def validate_context_archive_entries(entries: Iterable[str]) -> ContextArchiveSafetyReport:
    """Validate context archive entries for transfer safety."""

    return ContextArchiveSafetyReport(
        entries=[validate_archive_entry(entry) for entry in entries]
    )
