"""Models for read-only NAS/SMB shared artifact store scanning."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SharedStoreScanStatus(StrEnum):
    """Stable shared store scan statuses."""

    INDEXED = "indexed"
    ROOT_MISSING = "root-missing"
    BLOCKED = "blocked"
    ERROR = "error"


class SharedStoreLockStatus(StrEnum):
    """Read-only lock policy status."""

    NOT_REQUIRED = "not-required"
    LOCK_PRESENT = "lock-present"
    LOCK_MISSING = "lock-missing"
    LOCK_UNREADABLE = "lock-unreadable"


class SharedStoreFileStatus(StrEnum):
    """Per-file classification status."""

    SELECTED = "selected"
    OMITTED = "omitted"
    LARGE_METADATA_ONLY = "large-metadata-only"
    UNSAFE = "unsafe"


class SharedStoreFileRef(BaseModel):
    """One file discovered under a mounted shared store root."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    absolute_path: Path | None = None
    size: int = Field(default=0, ge=0)
    sha256: str | None = Field(default=None, min_length=64, max_length=64)
    content_type: str | None = None
    status: SharedStoreFileStatus
    omitted_reason: str | None = None
    safety_warnings: list[str] = Field(default_factory=list)


class SharedStoreScanRequest(BaseModel):
    """Input for a local mounted shared store scan."""

    model_config = ConfigDict(extra="forbid")

    mount_label: str = Field(min_length=1)
    root_path: Path
    selected_patterns: list[str] = Field(default_factory=list)
    max_file_size_bytes: int = Field(default=2_000_000, ge=1)
    compute_sha256: bool = True
    require_lock_file: bool = False
    lock_file_name: str = ".turingresearch_shared_store.lock"


class SharedStoreReport(BaseModel):
    """Report for read-only NAS/SMB shared artifact store scanning."""

    model_config = ConfigDict(extra="forbid")

    mount_label: str = Field(min_length=1)
    root_path: Path
    scan_status: SharedStoreScanStatus
    lock_status: SharedStoreLockStatus = SharedStoreLockStatus.NOT_REQUIRED
    scan_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    selected_files: list[SharedStoreFileRef] = Field(default_factory=list)
    omitted_files: list[SharedStoreFileRef] = Field(default_factory=list)
    large_files: list[SharedStoreFileRef] = Field(default_factory=list)
    unsafe_files: list[SharedStoreFileRef] = Field(default_factory=list)
    proposed_imports: list[dict[str, object]] = Field(default_factory=list)
    manifest: dict[str, str] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def reports_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("shared store reports require human review")
        if self.human_verified:
            raise ValueError("shared store artifacts are indexed, not verified")
        return self

    def to_markdown(self) -> str:
        """Render a concise Markdown review report."""

        lines = [
            f"# Shared Store Report: {self.mount_label}",
            "",
            f"- Root path: `{self.root_path}`",
            f"- Scan status: `{self.scan_status}`",
            f"- Lock status: `{self.lock_status}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            f"- Human verified: `{str(self.human_verified).lower()}`",
            "",
            "## Selected Files",
            "",
            *[
                f"- `{item.relative_path}` ({item.size} bytes)"
                for item in self.selected_files
            ],
            "",
            "## Large Files",
            "",
            *[f"- `{item.relative_path}`: {item.omitted_reason}" for item in self.large_files],
            "",
            "## Unsafe Files",
            "",
            *[f"- `{item.relative_path}`: {item.omitted_reason}" for item in self.unsafe_files],
            "",
            "## Proposed Imports",
            "",
            *[f"- {item}" for item in self.proposed_imports],
            "",
        ]
        return "\n".join(lines)
