"""Models for yogsoth-style convergence and stress-test parity."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StressScenarioId(StrEnum):
    """Supported review-only stress scenarios."""

    MISSING_EVIDENCE = "missing_evidence"
    FAKE_RESULT_RISK = "fake_result_risk"
    OVERCLAIM = "overclaim"
    ARTIFACT_MISSING = "artifact_missing"
    WEAK_RELATED_WORK = "weak_related_work"
    UNSAFE_PLUGIN = "unsafe_plugin"
    PRIVACY_LEAK = "privacy_leak"
    ROUTE_CONTRADICTION = "route_contradiction"
    ADVISOR_PACK_UNSUPPORTED_CLAIM = "advisor_pack_unsupported_claim"


class StressSeverity(StrEnum):
    """Stress-test finding severity."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class StressStatus(StrEnum):
    """Scenario result status."""

    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"


class StressTestInput(BaseModel):
    """Local input for deterministic stress testing."""

    model_config = ConfigDict(extra="forbid")

    target_id: str = Field(min_length=1)
    task_summary: str = Field(default="")
    evidence_refs: list[str] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    related_work_refs: list[str] = Field(default_factory=list)
    route_hard_gates: list[str] = Field(default_factory=list)
    route_forbidden_actions: list[str] = Field(default_factory=list)
    route_claims: list[str] = Field(default_factory=list)
    advisor_claims: list[str] = Field(default_factory=list)
    plugin_permissions: list[str] = Field(default_factory=list)
    text_blocks: list[str] = Field(default_factory=list)
    data_sensitivity: str = "demo"
    fake_demo_only: bool = True
    live_mode_enabled: bool = False


class StressScenario(BaseModel):
    """One scenario definition."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: StressScenarioId
    purpose: str = Field(min_length=1)
    risk_question: str = Field(min_length=1)
    default_severity: StressSeverity
    recommended_action: str = Field(min_length=1)


class StressFinding(BaseModel):
    """One stress-test finding."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: StressScenarioId
    status: StressStatus
    severity: StressSeverity
    message: str = Field(min_length=1)
    evidence: list[str] = Field(default_factory=list)
    recommended_action: str = Field(min_length=1)
    requires_human_review: bool = True


class StressTestReport(BaseModel):
    """Stress-test report for a route, release, advisor pack, or demo workflow."""

    model_config = ConfigDict(extra="forbid")

    target_id: str = Field(min_length=1)
    findings: list[StressFinding] = Field(default_factory=list)
    status: StressStatus
    blockers: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    convergence_recommendation: str = Field(min_length=1)
    requires_human_review: bool = True
    multi_agent_runtime: bool = False
    network_required: bool = False

    @model_validator(mode="after")
    def report_status_must_match_blockers(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("stress-test report requires human review")
        if self.blockers and self.status == StressStatus.PASS:
            raise ValueError("passing stress-test report cannot have blockers")
        return self
