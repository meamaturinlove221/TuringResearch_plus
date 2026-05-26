"""Models for dry-run repository split export."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RepoSplitStatus(StrEnum):
    """Dry-run split status."""

    PASS = "pass"
    PASS_WITH_WARNINGS = "pass-with-warnings"
    BLOCKED = "blocked"


class RepoSplitFileRecord(BaseModel):
    """One file considered for a dry-run split export."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    included: bool = True
    file_size: int | None = Field(default=None, ge=0)
    sha256: str | None = None
    omitted_reason: str | None = None
    safety_warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def omitted_file_requires_reason(self) -> Self:
        if not self.included and not self.omitted_reason:
            raise ValueError("omitted split export file requires omitted_reason")
        return self


class RepoSplitSafetyFinding(BaseModel):
    """One safety finding for a candidate split file."""

    model_config = ConfigDict(extra="forbid")

    relative_path: str = Field(min_length=1)
    finding_type: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    message: str = Field(min_length=1)
    release_blocker: bool = False
    requires_human_review: bool = True


class RepoSplitSafetyReport(BaseModel):
    """Safety report for a dry-run repository split export."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    checked_files: list[str] = Field(default_factory=list)
    findings: list[RepoSplitSafetyFinding] = Field(default_factory=list)
    omitted_files: list[RepoSplitFileRecord] = Field(default_factory=list)
    safe_to_export: bool = True
    release_blocker: bool = False
    requires_human_review: bool = True
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def summarize_safety_report(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("repo split safety reports require human review")
        self.release_blocker = any(finding.release_blocker for finding in self.findings)
        self.safe_to_export = not self.release_blocker
        return self


class RepoSplitManifest(BaseModel):
    """Manifest written into a dry-run split export."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    source_root: str = Field(min_length=1)
    export_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    dry_run_only: bool = True
    creates_github_repo: bool = False
    pushes_git: bool = False
    included_files: list[RepoSplitFileRecord] = Field(default_factory=list)
    omitted_files: list[RepoSplitFileRecord] = Field(default_factory=list)
    safety_report_path: str = "safety_report.md"
    requires_human_review: bool = True

    @model_validator(mode="after")
    def dry_run_manifest_never_pushes(self) -> Self:
        if not self.dry_run_only:
            raise ValueError("repo split exporter is dry-run only")
        if self.creates_github_repo or self.pushes_git:
            raise ValueError("repo split dry-run must not create GitHub repos or push git")
        if not self.requires_human_review:
            raise ValueError("repo split dry-run requires human review")
        return self


class RepoSplitDryRunRequest(BaseModel):
    """Input for a dry-run split export."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    source_root: Path
    output_root: Path
    file_paths: list[Path] = Field(default_factory=list)
    max_file_size_bytes: int = Field(default=500_000, ge=1)
    allowed_suffixes: set[str] = Field(
        default_factory=lambda: {".md", ".yaml", ".yml", ".json", ".txt", ".mmd", ".html"}
    )


class RepoSplitDryRunResult(BaseModel):
    """Result returned by the dry-run exporter."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    export_dir: Path
    manifest: RepoSplitManifest
    safety_report: RepoSplitSafetyReport
    status: RepoSplitStatus
