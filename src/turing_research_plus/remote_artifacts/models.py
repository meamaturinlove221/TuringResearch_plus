"""Unified remote artifact integration models."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class RemoteArtifactSourceKind(StrEnum):
    """Supported remote artifact source kinds."""

    GITHUB = "github"
    SSH_SFTP = "ssh_sftp"
    NAS_SMB = "nas_smb"
    CLOUD_OBJECT = "cloud_object"


class RemoteArtifactStatus(StrEnum):
    """Unified artifact status labels."""

    SELECTED = "selected"
    OMITTED = "omitted"
    METADATA_ONLY = "metadata-only"
    UNSAFE = "unsafe"
    ERROR = "error"


class RemoteArtifactSource(BaseModel):
    """One source contributing remote artifacts."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    kind: RemoteArtifactSourceKind
    label: str = Field(min_length=1)
    locator: str = Field(min_length=1)
    retrieval_status: str = "indexed"
    live_result: bool = False


class ArtifactRef(BaseModel):
    """Unified artifact reference normalized from remote artifact sources."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_kind: RemoteArtifactSourceKind
    path: str = Field(min_length=1)
    size: int = Field(default=0, ge=0)
    sha256: str | None = Field(default=None, min_length=8)
    content_type: str | None = None
    status: RemoteArtifactStatus
    omitted_reason: str | None = None
    safety_warnings: list[str] = Field(default_factory=list)
    evidence_tags: list[str] = Field(default_factory=list)
    human_verified: bool = False

    @model_validator(mode="after")
    def artifact_refs_are_not_verified(self) -> Self:
        if self.human_verified:
            raise ValueError("remote artifact refs are indexed, not verified")
        return self


class UnifiedRemoteArtifactReport(BaseModel):
    """Unified report across GitHub, SSH/SFTP, NAS/SMB, and object stores."""

    model_config = ConfigDict(extra="forbid")

    sources: list[RemoteArtifactSource] = Field(default_factory=list)
    normalized_artifacts: list[ArtifactRef] = Field(default_factory=list)
    duplicate_candidates: list[list[str]] = Field(default_factory=list)
    selected_artifacts: list[ArtifactRef] = Field(default_factory=list)
    omitted_artifacts: list[ArtifactRef] = Field(default_factory=list)
    unsafe_artifacts: list[ArtifactRef] = Field(default_factory=list)
    proposed_imports: list[dict[str, object]] = Field(default_factory=list)
    evidence_tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    requires_human_review: bool = True
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def unified_reports_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("unified remote artifact reports require human review")
        if self.human_verified:
            raise ValueError("remote artifact reports are indexed, not verified")
        return self

    def to_markdown(self) -> str:
        """Render a concise Markdown report."""

        lines = [
            "# Remote Artifact Integration Report",
            "",
            f"- Sources: `{len(self.sources)}`",
            f"- Normalized artifacts: `{len(self.normalized_artifacts)}`",
            f"- Requires human review: `{str(self.requires_human_review).lower()}`",
            f"- Human verified: `{str(self.human_verified).lower()}`",
            "",
            "## Selected Artifacts",
            "",
            *[
                f"- `{item.path}` from `{item.source_kind}` ({item.size} bytes)"
                for item in self.selected_artifacts
            ],
            "",
            "## Omitted Artifacts",
            "",
            *[
                f"- `{item.path}` from `{item.source_kind}`: {item.omitted_reason}"
                for item in self.omitted_artifacts
            ],
            "",
            "## Unsafe Artifacts",
            "",
            *[
                f"- `{item.path}` from `{item.source_kind}`: {item.omitted_reason}"
                for item in self.unsafe_artifacts
            ],
            "",
            "## Proposed Imports",
            "",
            *[f"- {item}" for item in self.proposed_imports],
            "",
        ]
        return "\n".join(lines)
