"""Reports for fake-first optional context pack transfer."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class TransferMode(StrEnum):
    """Supported transfer modes."""

    FAKE = "fake"
    SFTP = "sftp"


class TransferStatus(StrEnum):
    """Transfer runner status labels."""

    TRANSFERRED = "transferred"
    SKIPPED_LIVE_DISABLED = "skipped-live-disabled"
    SKIPPED_MISSING_CREDENTIAL = "skipped-missing-credential"
    BLOCKED = "blocked"


class TransferFileRecord(BaseModel):
    """One file selected or transferred by the runner."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    sha256: str | None = Field(default=None, min_length=64, max_length=64)
    size_bytes: int = 0
    source_path: str | None = None
    target_path: str | None = None
    transferred: bool = False
    warnings: list[str] = Field(default_factory=list)


class TransferOmittedFile(BaseModel):
    """One file omitted by transfer safety rules."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)


class TransferReport(BaseModel):
    """Review-only transfer report."""

    model_config = ConfigDict(extra="forbid")

    transfer_id: str = Field(min_length=1)
    package_id: str = Field(min_length=1)
    mode: TransferMode = TransferMode.FAKE
    status: TransferStatus
    source_dir: str = Field(min_length=1)
    target: str = Field(min_length=1)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    selected_files: list[TransferFileRecord] = Field(default_factory=list)
    omitted_files: list[TransferOmittedFile] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    live_enabled: bool = False
    credential_env: str | None = None
    remote_command_execution: bool = False
    remote_delete: bool = False
    remote_write_scope: str = "explicit_transfer_target_only"
    secrets_logged: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_transfer_safety(self) -> Self:
        if self.remote_command_execution:
            raise ValueError("transfer runner cannot execute remote commands")
        if self.remote_delete:
            raise ValueError("transfer runner cannot delete remote files")
        if self.secrets_logged:
            raise ValueError("transfer report cannot log secrets")
        if not self.requires_human_review:
            raise ValueError("transfer report requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether transfer result blocks handoff review."""

        return self.status == TransferStatus.BLOCKED or bool(self.errors)


def render_transfer_report(report: TransferReport) -> str:
    """Render a transfer report for human review."""

    lines = [
        f"# Transfer Report: {report.transfer_id}",
        "",
        f"- Package: `{report.package_id}`",
        f"- Mode: `{report.mode}`",
        f"- Status: `{report.status}`",
        f"- Source dir: `{report.source_dir}`",
        f"- Target: `{report.target}`",
        f"- Live enabled: `{str(report.live_enabled).lower()}`",
        "- Remote command execution: `false`",
        "- Remote delete: `false`",
        f"- Remote write scope: `{report.remote_write_scope}`",
        "- Secrets logged: `false`",
        "- Requires human review: `true`",
        "",
        "## Selected Files",
        "",
    ]
    lines.extend(
        [
            f"- `{item.path}` -> `{item.target_path or 'not-transferred'}`"
            for item in report.selected_files
        ]
        or ["- None."]
    )
    lines.extend(["", "## Omitted Files", ""])
    lines.extend(
        [f"- `{item.path}`: {item.reason}" for item in report.omitted_files]
        or ["- None."]
    )
    lines.extend(["", "## Errors", ""])
    lines.extend([f"- {item}" for item in report.errors] or ["- None."])
    return "\n".join(lines) + "\n"


def collect_source_files(source_dir: Path) -> list[Path]:
    """Return direct files from a context pack source directory."""

    if not source_dir.exists():
        return []
    return sorted(path for path in source_dir.iterdir() if path.is_file())
