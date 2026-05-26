"""Models for Markdown-first experiment run dashboards."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DashboardBadge(StrEnum):
    """Dashboard status badges."""

    REVIEW_READY_NOT_PROMOTED = "REVIEW_READY_NOT_PROMOTED"
    HARD_BLOCKED = "HARD_BLOCKED"
    ROUTE_EXHAUSTED = "ROUTE_EXHAUSTED"
    FAILED = "FAILED"
    PARTIAL = "PARTIAL"
    NOT_ENOUGH_EVIDENCE = "NOT_ENOUGH_EVIDENCE"
    REQUIRES_HUMAN_REVIEW = "REQUIRES_HUMAN_REVIEW"


class DashboardGateView(BaseModel):
    """Dashboard view of one hard gate."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    passed: bool
    reason: str = Field(min_length=1)


class DashboardArtifactCompleteness(BaseModel):
    """Artifact completeness summary."""

    model_config = ConfigDict(extra="forbid")

    present_count: int = Field(ge=0)
    missing_count: int = Field(ge=0)
    missing_artifacts: list[str] = Field(default_factory=list)


class RunDashboardReport(BaseModel):
    """Markdown-first Modal / experiment run dashboard report."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    run_status: str = Field(min_length=1)
    status_badges: list[DashboardBadge] = Field(default_factory=list)
    candidate_count: int = Field(ge=0)
    best_candidate: str | None = None
    backend_status: str = Field(min_length=1)
    hard_gates: list[DashboardGateView] = Field(default_factory=list)
    artifact_completeness: DashboardArtifactCompleteness
    visual_readiness: str = Field(min_length=1)
    failure_categories: list[str] = Field(default_factory=list)
    next_action: str = Field(min_length=1)
    advisor_readiness: str = Field(min_length=1)
    source_report: str | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    requires_human_review: bool = True
    experiment_executed_by_dashboard: bool = False
    human_verified: bool = False
    limitations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def dashboard_is_not_execution_result(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("run dashboard reports require human review")
        if self.experiment_executed_by_dashboard:
            raise ValueError("dashboard must not claim experiment execution")
        if self.human_verified:
            raise ValueError("dashboard displays ingested evidence, not verified results")
        return self
