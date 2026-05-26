"""Deep Insight workflow models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


class BoundaryConditionType(StrEnum):
    """Boundary condition validity type."""

    VALID = "valid"
    INVALID = "invalid"


class GapValidation(BaseModel):
    """Evidence-backed validation for one survey gap."""

    model_config = ConfigDict(extra="forbid")

    gap_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    validation_status: str = Field(default="validated", min_length=1)
    confidence: float = Field(default=0.7, ge=0.0, le=1.0)


class GapValidationReport(BaseModel):
    """Validated gap report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    gaps: list[GapValidation] = Field(min_length=1)

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert the report to a generic ResearchArtifact."""

        return ResearchArtifact(
            artifact_id=f"gap-validation-{self.report_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Gap Validation: {self.topic}",
            created_by="TuringResearch Plus insight",
            content=self.model_dump(mode="json"),
            evidence=[evidence for gap in self.gaps for evidence in gap.evidence],
            tags=["deep_insight", "gap_validation"],
        )


class InsightItem(BaseModel):
    """One synthesized insight with support and contradiction."""

    model_config = ConfigDict(extra="forbid")

    insight_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    supporting_evidence: list[EvidenceRef] = Field(min_length=1)
    contradicting_evidence: list[EvidenceRef] = Field(min_length=1)
    implication: str = Field(min_length=1)


class InsightReport(BaseModel):
    """Insight synthesis report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    insights: list[InsightItem] = Field(min_length=1)

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert the report to a generic ResearchArtifact."""

        evidence = [
            evidence
            for insight in self.insights
            for evidence in [*insight.supporting_evidence, *insight.contradicting_evidence]
        ]
        return ResearchArtifact(
            artifact_id=f"insight-{self.report_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Insight Report: {self.topic}",
            created_by="TuringResearch Plus insight",
            content=self.model_dump(mode="json"),
            evidence=evidence,
            tags=["deep_insight", "insight_report"],
        )


class BoundaryCondition(BaseModel):
    """A valid or invalid condition for a boundary map."""

    model_config = ConfigDict(extra="forbid")

    condition_id: str = Field(min_length=1)
    condition_type: BoundaryConditionType
    description: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)


class BoundaryMap(BaseModel):
    """Map of where a research claim applies or fails."""

    model_config = ConfigDict(extra="forbid")

    map_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    conditions: list[BoundaryCondition] = Field(min_length=2)

    @model_validator(mode="after")
    def require_valid_and_invalid_conditions(self) -> "BoundaryMap":
        condition_types = {condition.condition_type for condition in self.conditions}
        if BoundaryConditionType.VALID not in condition_types:
            raise ValueError("boundary map requires at least one valid condition")
        if BoundaryConditionType.INVALID not in condition_types:
            raise ValueError("boundary map requires at least one invalid condition")
        return self


class AssumptionSensitivity(BaseModel):
    """Sensitivity result for one assumption."""

    model_config = ConfigDict(extra="forbid")

    assumption_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    load_bearing: bool
    sensitivity: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)


class SensitivityReport(BaseModel):
    """Sensitivity probe report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    assumptions: list[AssumptionSensitivity] = Field(min_length=1)

    @model_validator(mode="after")
    def require_load_bearing_assumption(self) -> "SensitivityReport":
        if not any(assumption.load_bearing for assumption in self.assumptions):
            raise ValueError("sensitivity report requires a load-bearing assumption")
        return self


class ReformulatedProblem(BaseModel):
    """One problem reformulation."""

    model_config = ConfigDict(extra="forbid")

    problem_id: str = Field(min_length=1)
    original_problem: str = Field(min_length=1)
    reformulated_problem: str = Field(min_length=1)
    changes: list[str] = Field(min_length=1)
    invariants: list[str] = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)


class ReformulatedProblemSet(BaseModel):
    """Set of evidence-backed reformulated problems."""

    model_config = ConfigDict(extra="forbid")

    set_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    problems: list[ReformulatedProblem] = Field(min_length=1)


class DeepInsightResult(BaseModel):
    """Full Deep Insight workflow output."""

    model_config = ConfigDict(extra="forbid")

    gap_validation_report: GapValidationReport
    insight_report: InsightReport
    boundary_map: BoundaryMap
    sensitivity_report: SensitivityReport
    reformulated_problem_set: ReformulatedProblemSet

