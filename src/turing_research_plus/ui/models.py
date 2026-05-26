"""Models for lightweight static dashboard UI."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DashboardSectionKind(StrEnum):
    """Supported dashboard sections."""

    PROJECT_OVERVIEW = "project_overview"
    EVIDENCE_STATUS = "evidence_status"
    ARTIFACT_COMPLETENESS = "artifact_completeness"
    VISUAL_READINESS = "visual_readiness"
    RUN_DASHBOARD = "run_dashboard"
    RELATED_WORK = "related_work"
    FAILURE_TAXONOMY = "failure_taxonomy"
    ADVISOR_NEXT_ACTIONS = "advisor_next_actions"


class DashboardSection(BaseModel):
    """One static dashboard section."""

    model_config = ConfigDict(extra="forbid")

    kind: DashboardSectionKind
    title: str = Field(min_length=1)
    markdown: str = Field(min_length=1)
    source_path: str | None = None
    status: str = Field(default="requires-human-review", min_length=1)
    requires_human_review: bool = True


class StaticDashboardSpec(BaseModel):
    """Static dashboard spec rendered to Markdown and HTML."""

    model_config = ConfigDict(extra="forbid")

    dashboard_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    project_name: str = Field(min_length=1)
    sections: list[DashboardSection]
    output_dir: str
    generated_files: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    ui_executed_experiment: bool = False
    server_required: bool = False
    login_required: bool = False
    cloud_deployed: bool = False

    @model_validator(mode="after")
    def static_ui_boundaries(self) -> Self:
        if self.ui_executed_experiment:
            raise ValueError("dashboard UI must not claim experiment execution")
        if self.server_required:
            raise ValueError("minimal dashboard must not require a server")
        if self.login_required:
            raise ValueError("minimal dashboard must not require login")
        if self.cloud_deployed:
            raise ValueError("minimal dashboard must not claim cloud deployment")
        if not self.requires_human_review:
            raise ValueError("dashboard UI requires human review")
        return self


class StaticDashboardRequest(BaseModel):
    """Input paths for building a static VGGT dashboard."""

    model_config = ConfigDict(extra="forbid")

    dashboard_id: str = Field(default="vggt_static_dashboard", min_length=1)
    title: str = Field(default="VGGT Research Dashboard", min_length=1)
    project_name: str = Field(default="VGGT / SMPL-X Human Prior", min_length=1)
    output_dir: Path
    knowledge_pack_dir: Path
    advisor_pack_dir: Path
    run_dashboard_dir: Path
