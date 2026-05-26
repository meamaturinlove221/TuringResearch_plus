"""Models for fake-first SSH/SFTP remote artifact reading."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RemoteReaderSourceType(StrEnum):
    """Supported remote reader sources."""

    LOCAL_FIXTURE = "local_fixture"
    FAKE_SFTP = "fake_sftp"
    SFTP = "sftp"
    MANUAL_INDEX = "manual_index"


class RemoteReaderStatus(StrEnum):
    """Stable remote reader status labels."""

    INDEXED = "indexed"
    SELECTED = "selected"
    OMITTED = "omitted"
    RETRIEVED = "retrieved"
    LIVE_DISABLED = "live-disabled"
    MISSING_CREDENTIAL = "missing-credential"
    ERROR = "error"


class RemoteArtifactRecord(BaseModel):
    """One remote artifact record exposed by SFTP or a fixture."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    sha256: str | None = Field(default=None, min_length=64, max_length=64)
    is_dir: bool = False
    is_symlink: bool = False
    source_type: RemoteReaderSourceType = RemoteReaderSourceType.MANUAL_INDEX
    status: RemoteReaderStatus = RemoteReaderStatus.INDEXED
    modified_time: str | None = None
    warnings: list[str] = Field(default_factory=list)


class RemoteSelectedFile(BaseModel):
    """A selected small remote file or metadata-only record."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    sha256: str | None = Field(default=None, min_length=64, max_length=64)
    retrieval_status: RemoteReaderStatus = RemoteReaderStatus.SELECTED
    source_type: RemoteReaderSourceType
    local_path: Path | None = None
    verified: bool = False
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def selected_files_are_not_verified(self) -> Self:
        if self.verified:
            raise ValueError("remote reader never marks selected files verified")
        return self


class RemoteOmittedFile(BaseModel):
    """One omitted remote file."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    reason: str = Field(min_length=1)
    safety_warnings: list[str] = Field(default_factory=list)


class RemoteReaderRequest(BaseModel):
    """Input for the read-only SSH/SFTP remote reader."""

    model_config = ConfigDict(extra="forbid")

    host_label: str = Field(min_length=1)
    root_path: str = Field(min_length=1)
    fixture_index_path: Path | None = None
    selected_patterns: list[str] = Field(default_factory=list)
    dry_run: bool = True
    live_enabled: bool = False
    credential_env: str = "TURINGRESEARCH_SFTP_CREDENTIAL"
    max_file_size_bytes: int = Field(default=2_000_000, ge=1)
    allow_download: bool = False


class RemoteReaderReport(BaseModel):
    """Read-only remote artifact reader report."""

    model_config = ConfigDict(extra="forbid")

    host_label: str = Field(min_length=1)
    root_path: str = Field(min_length=1)
    retrieval_status: RemoteReaderStatus
    retrieval_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    scanned_paths: list[str] = Field(default_factory=list)
    artifact_list: list[RemoteArtifactRecord] = Field(default_factory=list)
    selected_files: list[RemoteSelectedFile] = Field(default_factory=list)
    omitted_files: list[RemoteOmittedFile] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    proposed_imports: list[dict[str, object]] = Field(default_factory=list)
    requires_human_review: bool = True
    live_result: bool = False
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def reports_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("remote reader reports require human review")
        if self.human_verified:
            raise ValueError("remote reader reports are retrieved, not verified")
        return self

    def to_markdown(self) -> str:
        """Render a concise Markdown review report."""

        lines = [
            f"# Remote Reader Report: {self.host_label}",
            "",
            f"- Root path: `{self.root_path}`",
            f"- Retrieval status: `{self.retrieval_status}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            f"- Human verified: `{str(self.human_verified).lower()}`",
            "- Verification boundary: remote artifacts are indexed or retrieved, "
            "not human verified.",
            "",
            "## Scanned Paths",
            "",
            *[f"- `{path}`" for path in self.scanned_paths],
            "",
            "## Selected Files",
            "",
            *[f"- `{item.path}` ({item.size} bytes)" for item in self.selected_files],
            "",
            "## Omitted Files",
            "",
            *[f"- `{item.path}`: {item.reason}" for item in self.omitted_files],
            "",
            "## Safety Warnings",
            "",
            *[f"- {warning}" for warning in self.safety_warnings],
            "",
            "## Proposed Imports",
            "",
            *[f"- {item}" for item in self.proposed_imports],
            "",
        ]
        return "\n".join(lines)
