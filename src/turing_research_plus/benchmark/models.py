"""Models for benchmark and replay scenarios."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class BenchmarkStatus(StrEnum):
    """Replay outcome labels."""

    PASS = "pass"
    PARTIAL = "partial"
    FAIL = "fail"
    SKIPPED = "skipped"


class BenchmarkStep(BaseModel):
    """One replay step that checks local expected outputs."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    expected_outputs: list[str] = Field(default_factory=list)
    demo_only: bool = True


class BenchmarkScenario(BaseModel):
    """A local benchmark replay scenario."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    root_path: str = Field(min_length=1)
    steps: list[BenchmarkStep] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)
    no_real_experiment: bool = True
    network_required: bool = False
    demo_only: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def scenario_stays_fake_default(self) -> Self:
        if self.network_required:
            raise ValueError("benchmark replay scenario must not require network")
        if not self.no_real_experiment:
            raise ValueError("benchmark replay scenario must not run real experiments")
        if not self.demo_only:
            raise ValueError("benchmark replay scenario must be demo-only")
        if not self.requires_human_review:
            raise ValueError("benchmark replay scenario requires human review")
        return self


class BenchmarkReport(BaseModel):
    """Report from a benchmark replay."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str = Field(min_length=1)
    steps: list[BenchmarkStep] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)
    actual_outputs: list[str] = Field(default_factory=list)
    missing_outputs: list[str] = Field(default_factory=list)
    status: BenchmarkStatus
    duration: float | None = None
    warnings: list[str] = Field(default_factory=list)
    regression_flags: list[str] = Field(default_factory=list)
    demo_only: bool = True
    no_real_experiment: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def report_stays_replay_only(self) -> Self:
        if not self.demo_only:
            raise ValueError("benchmark report must stay demo-only")
        if not self.no_real_experiment:
            raise ValueError("benchmark report must not represent real experiments")
        if not self.requires_human_review:
            raise ValueError("benchmark report requires human review")
        return self
