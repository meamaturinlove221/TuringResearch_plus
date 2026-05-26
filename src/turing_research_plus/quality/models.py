"""Models for quality metrics and regression gates."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class QualityStatus(StrEnum):
    """Quality metric status labels."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class QualityMetric(BaseModel):
    """One quality metric result."""

    model_config = ConfigDict(extra="forbid")

    metric_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=1.0)
    status: QualityStatus
    details: list[str] = Field(default_factory=list)


class QualityReport(BaseModel):
    """Quality report over docs, tests, contracts, examples, and safety."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    metrics: list[QualityMetric] = Field(default_factory=list)
    status: QualityStatus
    warnings: list[str] = Field(default_factory=list)
    release_ready: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def report_requires_review_and_consistent_status(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("quality report requires human review")
        if self.release_ready and self.status != QualityStatus.PASS:
            raise ValueError("release_ready requires passing quality status")
        return self


class RegressionGateCheck(BaseModel):
    """One regression gate check."""

    model_config = ConfigDict(extra="forbid")

    check_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    passed: bool
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class RegressionGateReport(BaseModel):
    """Regression gate report."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    checks: list[RegressionGateCheck] = Field(default_factory=list)
    status: QualityStatus
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    requires_human_review: bool = True

    @model_validator(mode="after")
    def gate_status_matches_blockers(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("regression gate requires human review")
        if self.blockers and self.status == QualityStatus.PASS:
            raise ValueError("passing regression gate cannot have blockers")
        return self
