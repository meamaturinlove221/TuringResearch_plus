"""Subtask boundary models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tuling_research_plus.artifacts.models import ResearchArtifact


class SubtaskStatus(StrEnum):
    """Subtask status values."""

    PLANNED = "planned"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


class SubtaskExecutionMode(StrEnum):
    """Supported subtask execution modes."""

    MANUAL_CODEX_ROLE = "manual_codex_role"
    LLM_CLIENT = "llm_client"
    DRY_RUN = "dry_run"


class SubtaskErrorCode(StrEnum):
    """Typed subtask runtime error codes."""

    QUALITY_GATE_FAILED = "quality_gate_failed"
    UNSUPPORTED_EXECUTION_MODE = "unsupported_execution_mode"


class SubtaskError(BaseModel):
    """Typed subtask runtime error."""

    model_config = ConfigDict(extra="forbid")

    code: SubtaskErrorCode
    message: str = Field(min_length=1)


class SubtaskSpec(BaseModel):
    """Minimal subtask specification for future workflow orchestration."""

    model_config = ConfigDict(extra="forbid")

    subtask_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    status: SubtaskStatus = SubtaskStatus.PLANNED
    depends_on: list[str] = Field(default_factory=list)
    inputs: dict[str, Any] = Field(default_factory=dict)


class TaskProfile(BaseModel):
    """Runtime profile for a delegated or fake subtask."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    role: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    allowed_tools: list[str] = Field(default_factory=list)
    reasoning_style: str = Field(default="concise", min_length=1)
    quality_gate: str | None = None
    profile_id: str | None = None
    max_steps: int = Field(default=1, gt=0)
    dry_run: bool = True

    @model_validator(mode="after")
    def validate_profile(self) -> "TaskProfile":
        if not self.dry_run and not self.allowed_tools:
            msg = "non-dry-run TaskProfile requires allowed_tools"
            raise ValueError(msg)
        if self.profile_id is None:
            self.profile_id = self.name
        return self


class SubtaskResult(BaseModel):
    """Result returned by SubtaskRunner."""

    model_config = ConfigDict(extra="forbid")

    subtask_id: str = Field(min_length=1)
    status: SubtaskStatus
    artifacts: list[ResearchArtifact] = Field(default_factory=list)
    message: str = ""
    rendered_prompt: str | None = None
    error: SubtaskError | None = None
