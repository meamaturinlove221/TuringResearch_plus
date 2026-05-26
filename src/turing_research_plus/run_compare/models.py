"""Models for metadata-level run and board comparison."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BoardStatus(StrEnum):
    """Board availability status."""

    AVAILABLE = "available"
    MISSING = "missing"
    PROXY_ONLY = "proxy-only"
    REQUIRES_REVIEW = "requires-human-review"


class RunComparisonStatus(StrEnum):
    """Run-level status for comparison reports."""

    OBSERVED = "observed"
    LOCAL_OBSERVED = "local-observed"
    PLANNED = "planned"
    HARD_BLOCKED = "hard-blocked"
    NOT_ENOUGH_EVIDENCE = "not-enough-evidence"
    REQUIRES_HUMAN_REVIEW = "requires-human-review"


class BoardRef(BaseModel):
    """One visual board or board-like artifact."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    board_id: str = Field(min_length=1)
    path: str | None = None
    status: BoardStatus = BoardStatus.MISSING
    board_type: str = Field(default="unknown", min_length=1)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class RunComparisonInput(BaseModel):
    """Minimal run metadata used for comparison."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    route_id: str | None = None
    status: RunComparisonStatus = RunComparisonStatus.REQUIRES_HUMAN_REVIEW
    boards: list[BoardRef] = Field(default_factory=list)
    artifacts_present: list[str] = Field(default_factory=list)
    artifacts_missing: list[str] = Field(default_factory=list)
    hard_gates_passed: list[str] = Field(default_factory=list)
    hard_gates_failed: list[str] = Field(default_factory=list)
    failure_categories: list[str] = Field(default_factory=list)
    claimed_improvements: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def comparison_inputs_require_review(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("run comparison inputs require human review")
        return self


class ArtifactCompletenessEntry(BaseModel):
    """Artifact completeness for one run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    present_count: int = Field(ge=0)
    missing_count: int = Field(ge=0)
    missing_artifacts: list[str] = Field(default_factory=list)


class VisualCompletenessEntry(BaseModel):
    """Visual board completeness for one run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    available_count: int = Field(ge=0)
    missing_count: int = Field(ge=0)
    proxy_only_count: int = Field(ge=0)
    warnings: list[str] = Field(default_factory=list)


class HardGateSummaryEntry(BaseModel):
    """Hard-gate comparison summary for one run."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    passed: list[str] = Field(default_factory=list)
    failed: list[str] = Field(default_factory=list)


class RunComparisonReport(BaseModel):
    """Metadata-only comparison report across experiment runs."""

    model_config = ConfigDict(extra="forbid")

    compared_runs: list[str] = Field(default_factory=list)
    available_boards: list[BoardRef] = Field(default_factory=list)
    missing_boards: list[BoardRef] = Field(default_factory=list)
    artifact_completeness: list[ArtifactCompletenessEntry] = Field(default_factory=list)
    visual_completeness: list[VisualCompletenessEntry] = Field(default_factory=list)
    hard_gate_summary: list[HardGateSummaryEntry] = Field(default_factory=list)
    failure_summary: dict[str, list[str]] = Field(default_factory=dict)
    claimed_improvements: list[str] = Field(default_factory=list)
    unsupported_claims: list[str] = Field(default_factory=list)
    next_actions: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    image_understanding_performed: bool = False

    @model_validator(mode="after")
    def report_is_metadata_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("run comparison reports require human review")
        if self.image_understanding_performed:
            raise ValueError("run comparison must not claim image understanding")
        return self
