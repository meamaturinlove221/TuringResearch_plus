"""Cross-platform archive notes for Session runtime handoff packages."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.session_runtime.path_normalization import (
    windows_path_to_posix,
)

NO_SAME_OWNER_NOTE = (
    "Do not preserve archive ownership during manual unpack; avoid --same-owner "
    "and prefer the current local user for review directories."
)
SYMLINK_POLICY_NOTE = (
    "Symlink members are blocked by default; if a future manual workflow allows "
    "them, the link target must be relative, normalized, and separately reviewed."
)


class ArchivePlatformNotes(BaseModel):
    """Human-readable platform notes for archive creation and unpack."""

    model_config = ConfigDict(extra="forbid")

    archive_format: str = "directory-or-tar-compatible"
    windows_path_policy: str = "Windows separators are normalized to POSIX archive paths."
    linux_unpack_policy: str = "Linux unpack must validate members before ingest review."
    dotfile_policy: str = "Hidden dotfiles are denied unless explicitly allowlisted."
    no_same_owner_note: str = NO_SAME_OWNER_NOTE
    symlink_policy: str = SYMLINK_POLICY_NOTE
    checksum_policy: str = "Validate checksums before ingest or evidence review."
    return_archive_policy: str = (
        "Return archives must pass member, checksum, and safety validation."
    )
    live_execution_policy: str = (
        "Archive handling never enables remote command execution by default."
    )
    examples: list[str] = Field(
        default_factory=lambda: [
            "PROJECT_CONTEXT.md",
            "nested/ROUTE_SPEC.yaml",
            "returns/FINAL_STATUS.json",
        ]
    )


def build_archive_platform_notes() -> ArchivePlatformNotes:
    """Return the current cross-platform archive hardening notes."""

    return ArchivePlatformNotes()


def normalize_platform_archive_path(path: str) -> str:
    """Normalize a platform-specific path spelling to POSIX archive style."""

    return windows_path_to_posix(path)


def render_archive_platform_notes(notes: ArchivePlatformNotes | None = None) -> str:
    """Render platform notes as Markdown."""

    data = notes or build_archive_platform_notes()
    lines = [
        "# Cross-platform Archive Notes",
        "",
        f"- Archive format: {data.archive_format}",
        f"- Windows path policy: {data.windows_path_policy}",
        f"- Linux unpack policy: {data.linux_unpack_policy}",
        f"- Dotfile policy: {data.dotfile_policy}",
        f"- Ownership policy: {data.no_same_owner_note}",
        f"- Symlink policy: {data.symlink_policy}",
        f"- Checksum policy: {data.checksum_policy}",
        f"- Return archive policy: {data.return_archive_policy}",
        f"- Live execution policy: {data.live_execution_policy}",
    ]
    return "\n".join(lines) + "\n"
