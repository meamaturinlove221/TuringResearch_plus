"""Models for local session preflight runtime checks."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.pod_lifecycle import PodContextLifecycle


class SessionPreflightStatus(StrEnum):
    """Status for local session preflight reports."""

    PASS = "pass"
    PASS_WITH_WARNINGS = "pass-with-warnings"
    BLOCKED = "blocked"


class SessionPreflightFindingSeverity(StrEnum):
    """Finding severity levels."""

    INFO = "info"
    WARNING = "warning"
    BLOCKER = "blocker"


class SessionEnvironmentCheck(BaseModel):
    """One environment check result."""

    model_config = ConfigDict(extra="forbid")

    check_id: str = Field(min_length=1)
    status: SessionPreflightStatus
    message: str = Field(min_length=1)
    path: str | None = None
    release_blocker: bool = False


class SessionPreflightFinding(BaseModel):
    """One preflight finding."""

    model_config = ConfigDict(extra="forbid")

    finding_id: str = Field(min_length=1)
    severity: SessionPreflightFindingSeverity
    message: str = Field(min_length=1)
    path: str | None = None
    release_blocker: bool = False


class SessionLookupRecord(BaseModel):
    """Resolved local paths and context file list for a session preflight."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    project_root: str = Field(min_length=1)
    context_source: str = Field(min_length=1)
    output_dir: str = Field(min_length=1)
    context_files: list[str] = Field(default_factory=list)


class SessionPreflightRequest(BaseModel):
    """Request for a local session preflight check."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    session_id: str = Field(min_length=1)
    project_root: Path
    context_source: Path
    output_dir: Path
    lifecycle: PodContextLifecycle
    candidate_paths: list[str] = Field(default_factory=list)
    source_platform: str = "Windows"
    target_platform: str = "Linux pod"
    archive_format: str = "tar"
    allow_raw_data: bool = False
    remote_execution_enabled: bool = False
    live_network_enabled: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_local_review_only(self) -> Self:
        if self.remote_execution_enabled:
            raise ValueError("session preflight cannot enable remote execution")
        if self.live_network_enabled:
            raise ValueError("session preflight cannot enable live networking")
        if not self.requires_human_review:
            raise ValueError("session preflight requires human review")
        return self


class SessionPreflightReport(BaseModel):
    """Review-only local session preflight report."""

    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(min_length=1)
    context_package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    status: SessionPreflightStatus
    lookup: SessionLookupRecord
    environment_checks: list[SessionEnvironmentCheck] = Field(default_factory=list)
    findings: list[SessionPreflightFinding] = Field(default_factory=list)
    checked_paths: list[str] = Field(default_factory=list)
    platform_warnings: list[str] = Field(default_factory=list)
    remote_execution_enabled: bool = False
    live_network_enabled: bool = False
    proposed_updates_only: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_report_boundary(self) -> Self:
        if self.remote_execution_enabled:
            raise ValueError("session preflight report cannot enable remote execution")
        if self.live_network_enabled:
            raise ValueError("session preflight report cannot enable live networking")
        if not self.proposed_updates_only:
            raise ValueError("session preflight report must keep proposed updates only")
        if not self.requires_human_review:
            raise ValueError("session preflight report requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether this preflight blocks session handoff."""

        return any(check.release_blocker for check in self.environment_checks) or any(
            finding.release_blocker for finding in self.findings
        )
