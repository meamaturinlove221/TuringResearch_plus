"""Safe experiment execution planning models."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ExecutionPlanStatus(StrEnum):
    """Status for safe execution plans."""

    PLANNED = "planned"
    BLOCKED = "blocked"
    READY_FOR_HUMAN_RUN = "ready-for-human-run"


class ArtifactRequirement(BaseModel):
    """One artifact required before a run can be reviewed."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    required: bool = True
    source_stage_id: str | None = None
    acceptance_criteria: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class RunIngestContract(BaseModel):
    """Contract for ingesting a run after a human executes it elsewhere."""

    model_config = ConfigDict(extra="forbid")

    route_id: str = Field(min_length=1)
    accepted_source_types: list[str] = Field(default_factory=list)
    required_metadata: list[str] = Field(default_factory=list)
    required_artifacts: list[str] = Field(default_factory=list)
    proposed_evidence_only: bool = True
    writes_observed_result: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def ingest_contract_must_not_write_observed_results(self) -> Self:
        if self.writes_observed_result:
            raise ValueError("run ingest contract must not write observed results")
        return self


class ExperimentExecutionPlan(BaseModel):
    """Review-only execution plan and runbook payload."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    status: ExecutionPlanStatus = ExecutionPlanStatus.PLANNED
    runbook_steps: list[str] = Field(default_factory=list)
    artifact_requirements: list[ArtifactRequirement] = Field(default_factory=list)
    hard_gates: list[str] = Field(default_factory=list)
    forbidden_actions: list[str] = Field(default_factory=list)
    ingest_contract: RunIngestContract
    blockers: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    automatically_executes: bool = False
    remote_execution: bool = False
    modal_call: bool = False
    gpu_call: bool = False
    writes_observed_result: bool = False

    @model_validator(mode="after")
    def plan_must_keep_execution_disabled(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("experiment execution plan requires human review")
        if (
            self.automatically_executes
            or self.remote_execution
            or self.modal_call
            or self.gpu_call
            or self.writes_observed_result
        ):
            raise ValueError("safe execution plan cannot execute or write observed results")
        if self.blockers and self.status == ExecutionPlanStatus.READY_FOR_HUMAN_RUN:
            raise ValueError("ready plan cannot have blockers")
        return self
