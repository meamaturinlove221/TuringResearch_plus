"""Stress Test workflow models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


class Severity(StrEnum):
    """Stress-test finding severity."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


class PassFail(StrEnum):
    """Stress-test outcome."""

    PASS = "pass"
    FAIL = "fail"


class Claim(BaseModel):
    """Claim boundary object for red-team checks."""

    model_config = ConfigDict(extra="forbid")

    claim_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class ExperimentPlan(BaseModel):
    """Minimal experiment plan for premortem checks."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    hypothesis_link: str = Field(min_length=1)
    design: str = Field(min_length=1)
    required_data: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    controls: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class StressWeakness(BaseModel):
    """One stress-test weakness."""

    model_config = ConfigDict(extra="forbid")

    weakness_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: Severity
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class FailureMode(BaseModel):
    """One failure mode."""

    model_config = ConfigDict(extra="forbid")

    mode_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    severity: Severity
    mitigation: str | None = None


class StressTestReport(BaseModel):
    """Unified stress-test report."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str = Field(min_length=1)
    weaknesses: list[StressWeakness] = Field(default_factory=list)
    severity: Severity
    attack_paths: list[str] = Field(default_factory=list)
    counterarguments: list[str] = Field(default_factory=list)
    failure_modes: list[FailureMode] = Field(default_factory=list)
    mitigations: list[str] = Field(default_factory=list)
    residual_risk: Severity
    pass_fail: PassFail
    rerun_recommendations: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def fail_on_high_or_critical_residual_risk(self) -> "StressTestReport":
        if self.residual_risk in {Severity.CRITICAL, Severity.HIGH}:
            object.__setattr__(self, "pass_fail", PassFail.FAIL)
        return self

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert report to a ResearchArtifact."""

        evidence = [
            evidence
            for weakness in self.weaknesses
            for evidence in weakness.evidence_refs
        ]
        if not evidence:
            evidence = [
                EvidenceRef(
                    source_id=f"stress:{self.artifact_id}",
                    locator="stress-test",
                    quote="Stress test produced structural findings without source evidence.",
                    confidence=0.4,
                )
            ]
        return ResearchArtifact(
            artifact_id=f"stress-{self.artifact_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Stress Test: {self.artifact_id}",
            created_by="TuringResearch Plus stress",
            content=self.model_dump(mode="json"),
            evidence=evidence,
            tags=["stress_test", self.pass_fail],
        )


def max_severity(values: list[Severity]) -> Severity:
    """Return the highest severity."""

    order = {
        Severity.INFORMATIONAL: 0,
        Severity.LOW: 1,
        Severity.MEDIUM: 2,
        Severity.HIGH: 3,
        Severity.CRITICAL: 4,
    }
    if not values:
        return Severity.INFORMATIONAL
    return max(values, key=lambda severity: order[severity])


def pass_fail_from_risk(severity: Severity) -> PassFail:
    """Return pass/fail from residual severity."""

    if severity in {Severity.LOW, Severity.INFORMATIONAL}:
        return PassFail.PASS
    return PassFail.FAIL
