"""Models for fake-first GitHub artifact sync."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class GitHubArtifactSourceType(StrEnum):
    """Supported GitHub artifact surfaces."""

    LOCAL_FIXTURE = "local_fixture"
    RELEASE_ASSET = "release_asset"
    WORKFLOW_ARTIFACT = "workflow_artifact"
    PRIVATE_REPO_INDEX = "private_repo_index"
    MANUAL_INDEX = "manual_index"


class GitHubArtifactStatus(StrEnum):
    """Stable artifact sync statuses."""

    INDEXED = "indexed"
    SELECTED = "selected"
    OMITTED = "omitted"
    RETRIEVED = "retrieved"
    LIVE_DISABLED = "live-disabled"
    MISSING_TOKEN = "missing-token"
    ERROR = "error"


class GitHubArtifactRecord(BaseModel):
    """One artifact exposed by GitHub or a local fixture."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    path: str = Field(min_length=1)
    source_type: GitHubArtifactSourceType = GitHubArtifactSourceType.MANUAL_INDEX
    size: int = Field(default=0, ge=0)
    sha256: str | None = Field(default=None, min_length=64, max_length=64)
    download_url: str | None = None
    content_type: str | None = None
    status: GitHubArtifactStatus = GitHubArtifactStatus.INDEXED
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class GitHubSelectedFile(BaseModel):
    """A small selected file or selected metadata record."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    sha256: str | None = Field(default=None, min_length=64, max_length=64)
    source_type: GitHubArtifactSourceType
    retrieval_status: GitHubArtifactStatus = GitHubArtifactStatus.SELECTED
    local_path: Path | None = None
    verified: bool = False
    warnings: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def selected_files_are_not_verified(self) -> Self:
        if self.verified:
            raise ValueError("GitHub artifact sync never marks selected files verified")
        return self


class GitHubOmittedFile(BaseModel):
    """One omitted remote artifact."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    reason: str = Field(min_length=1)
    safety_warnings: list[str] = Field(default_factory=list)


class GitHubArtifactSyncRequest(BaseModel):
    """Input for GitHub artifact sync."""

    model_config = ConfigDict(extra="forbid")

    source_repo: str = Field(min_length=1)
    source_ref: str = Field(default="main", min_length=1)
    fixture_index_path: Path | None = None
    selected_patterns: list[str] = Field(default_factory=list)
    output_dir: Path | None = None
    dry_run: bool = True
    live_enabled: bool = False
    token_env: str = "GITHUB_TOKEN"
    max_file_size_bytes: int = Field(default=2_000_000, ge=1)
    allow_download: bool = False


class GitHubArtifactSyncReport(BaseModel):
    """Report for GitHub artifact sync."""

    model_config = ConfigDict(extra="forbid")

    source_repo: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    retrieval_status: GitHubArtifactStatus
    retrieval_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    artifact_list: list[GitHubArtifactRecord] = Field(default_factory=list)
    selected_files: list[GitHubSelectedFile] = Field(default_factory=list)
    omitted_files: list[GitHubOmittedFile] = Field(default_factory=list)
    sha256: dict[str, str] = Field(default_factory=dict)
    size: dict[str, int] = Field(default_factory=dict)
    safety_warnings: list[str] = Field(default_factory=list)
    proposed_imports: list[dict[str, object]] = Field(default_factory=list)
    requires_human_review: bool = True
    live_result: bool = False
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def sync_reports_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("GitHub artifact sync reports require human review")
        if self.human_verified:
            raise ValueError("GitHub artifact sync reports are retrieved, not verified")
        return self

    def to_markdown(self) -> str:
        """Render a concise Markdown review report."""

        lines = [
            f"# GitHub Artifact Sync Report: {self.source_repo}",
            "",
            f"- Source ref: `{self.source_ref}`",
            f"- Retrieval status: `{self.retrieval_status}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            f"- Human verified: `{str(self.human_verified).lower()}`",
            "- Verification boundary: retrieved metadata and selected files are "
            "not human verified.",
            "",
            "## Selected Files",
            "",
            *[f"- `{item.path}` ({item.size} bytes)" for item in self.selected_files],
            "",
            "## Omitted Files",
            "",
            *[
                f"- `{item.path}`: {item.reason}"
                for item in self.omitted_files
            ],
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
