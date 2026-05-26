"""Models for multi-project workspaces."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProjectType(StrEnum):
    """Supported project types for workspace indexing."""

    VGGT_CASE_STUDY = "vggt_case_study"
    DEMO_RESEARCH = "demo_research"
    PAPER_SURVEY = "paper_survey"
    EXPERIMENTAL = "experimental"
    TEMPLATE = "template"
    UNKNOWN = "unknown"


class ProjectStatus(StrEnum):
    """Project-level review status."""

    ACTIVE = "active"
    PLANNED = "planned"
    DEMO_ONLY = "demo-only"
    BLOCKED = "blocked"
    ARCHIVED = "archived"
    UNKNOWN = "unknown"


class ProjectPrivacyLevel(StrEnum):
    """Project-level privacy classification."""

    PUBLIC_DEMO = "public-demo"
    INTERNAL = "internal"
    PRIVATE = "private"
    RESTRICTED = "restricted"


class WorkspaceProject(BaseModel):
    """One project entry in a multi-project workspace."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    project_type: ProjectType = ProjectType.UNKNOWN
    project_root: Path
    docs_path: Path | None = None
    evidence_path: Path | None = None
    artifacts_path: Path | None = None
    advisor_pack_path: Path | None = None
    routes_path: Path | None = None
    status: ProjectStatus = ProjectStatus.UNKNOWN
    privacy_level: ProjectPrivacyLevel = ProjectPrivacyLevel.INTERNAL
    tags: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    fake_demo: bool = False
    human_verified: bool = False

    @model_validator(mode="after")
    def workspace_project_preserves_review_boundaries(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("workspace projects require human review")
        if self.human_verified:
            raise ValueError("workspace index is not a verified evidence source")
        if any(part in self.project_id for part in ["..", "/", "\\", ":"]):
            raise ValueError("project_id must be a simple path-safe slug")
        if self.status == ProjectStatus.DEMO_ONLY and not self.fake_demo:
            raise ValueError("demo-only projects must be marked fake_demo")
        return self


class Workspace(BaseModel):
    """A local registry of multiple research projects."""

    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(min_length=1)
    workspace_name: str = Field(min_length=1)
    workspace_root: Path
    projects: list[WorkspaceProject] = Field(default_factory=list)
    status: ProjectStatus = ProjectStatus.ACTIVE
    privacy_level: ProjectPrivacyLevel = ProjectPrivacyLevel.INTERNAL
    requires_human_review: bool = True
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def workspace_preserves_boundaries(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("workspaces require human review")
        if self.human_verified:
            raise ValueError("workspace registry is not a verified evidence source")
        project_ids = [project.project_id for project in self.projects]
        if len(set(project_ids)) != len(project_ids):
            raise ValueError("workspace project_id values must be unique")
        return self


class WorkspaceProjectSummary(BaseModel):
    """Summary for one indexed project."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    project_type: ProjectType
    status: ProjectStatus
    privacy_level: ProjectPrivacyLevel
    existing_paths: list[str] = Field(default_factory=list)
    missing_paths: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    fake_demo: bool = False
    evidence_source: bool = False

    @model_validator(mode="after")
    def summaries_are_not_evidence_sources(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("workspace project summaries require human review")
        if self.evidence_source:
            raise ValueError("workspace summaries are not evidence sources")
        return self


class WorkspaceOverview(BaseModel):
    """High-level overview for a workspace registry."""

    model_config = ConfigDict(extra="forbid")

    workspace_id: str = Field(min_length=1)
    workspace_name: str = Field(min_length=1)
    project_count: int = Field(ge=0)
    projects: list[WorkspaceProjectSummary] = Field(default_factory=list)
    missing_paths: dict[str, list[str]] = Field(default_factory=dict)
    safety_warnings: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    evidence_source: bool = False

    @model_validator(mode="after")
    def overview_is_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("workspace overview requires human review")
        if self.evidence_source:
            raise ValueError("workspace overview is not an evidence source")
        return self


class WorkspaceContext(BaseModel):
    """Loaded local context snippets for one workspace project."""

    model_config = ConfigDict(extra="forbid")

    project_id: str = Field(min_length=1)
    loaded_files: dict[str, str] = Field(default_factory=dict)
    missing_files: list[str] = Field(default_factory=list)
    safety_warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    evidence_source: bool = False

    @model_validator(mode="after")
    def context_is_not_evidence_source(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("workspace context requires human review")
        if self.evidence_source:
            raise ValueError("workspace context is not an evidence source")
        return self
