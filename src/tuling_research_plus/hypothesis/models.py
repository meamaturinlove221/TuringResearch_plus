"""Hypothesis Formation workflow models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tuling_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


class RiskLevel(StrEnum):
    """Hypothesis risk level."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class GapPriority(BaseModel):
    """Prioritized validated gap."""

    model_config = ConfigDict(extra="forbid")

    gap_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    score: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)


class GapPriorityReport(BaseModel):
    """Ranked gap priority report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    priorities: list[GapPriority] = Field(min_length=1)

    @model_validator(mode="after")
    def sort_priorities(self) -> "GapPriorityReport":
        self.priorities.sort(key=lambda priority: priority.score, reverse=True)
        return self


class FalsifiabilityCriteria(BaseModel):
    """Criteria that make a hypothesis falsifiable."""

    model_config = ConfigDict(extra="forbid")

    observable_prediction: str = Field(min_length=1)
    falsifying_observation: str = Field(min_length=1)
    measurement_window: str = Field(min_length=1)
    minimum_test: str = Field(min_length=1)


class ExperimentRequirement(BaseModel):
    """Required experiment plan placeholder."""

    model_config = ConfigDict(extra="forbid")

    design: str = Field(min_length=1)
    required_data: list[str] = Field(min_length=1)
    measurement: str = Field(min_length=1)


class Hypothesis(BaseModel):
    """Ranked falsifiable hypothesis."""

    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    independent_variables: list[str] = Field(min_length=1)
    dependent_variables: list[str] = Field(min_length=1)
    control_variables: list[str] = Field(min_length=1)
    falsifiability_criteria: FalsifiabilityCriteria
    success_criteria: list[str] = Field(min_length=1)
    failure_interpretation: str = Field(min_length=1)
    required_experiment: ExperimentRequirement
    boundary_conditions: list[str] = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)
    risk_level: RiskLevel
    score: float = Field(default=0.0, ge=0.0, le=1.0)


class HypothesisSet(BaseModel):
    """Generated hypothesis set."""

    model_config = ConfigDict(extra="forbid")

    set_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    hypotheses: list[Hypothesis] = Field(min_length=1)

    @model_validator(mode="after")
    def sort_hypotheses(self) -> "HypothesisSet":
        self.hypotheses.sort(key=lambda hypothesis: hypothesis.score, reverse=True)
        return self


class OperationalizedHypothesis(BaseModel):
    """Operationalized hypothesis with concrete variable plan."""

    model_config = ConfigDict(extra="forbid")

    hypothesis_id: str = Field(min_length=1)
    variables: dict[str, list[str]] = Field(min_length=1)
    measurement_plan: str = Field(min_length=1)
    experiment_readiness: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)


class ResearchQuestion(BaseModel):
    """Precise research question derived from a hypothesis."""

    model_config = ConfigDict(extra="forbid")

    question_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
    hypothesis_id: str = Field(min_length=1)
    finer_score: float = Field(ge=0.0, le=1.0)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)


class FINERAssessment(BaseModel):
    """FINER score for a research question."""

    model_config = ConfigDict(extra="forbid")

    feasible: float = Field(ge=0.0, le=1.0)
    interesting: float = Field(ge=0.0, le=1.0)
    novel: float = Field(ge=0.0, le=1.0)
    ethical: float = Field(ge=0.0, le=1.0)
    relevant: float = Field(ge=0.0, le=1.0)
    overall: float = Field(ge=0.0, le=1.0)


class HypothesisPortfolio(BaseModel):
    """Selected hypothesis portfolio."""

    model_config = ConfigDict(extra="forbid")

    portfolio_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    selected: list[Hypothesis] = Field(min_length=1)
    research_questions: list[ResearchQuestion] = Field(min_length=1)
    rationale: str = Field(min_length=1)

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert the portfolio to a generic ResearchArtifact."""

        return ResearchArtifact(
            artifact_id=f"hypothesis-portfolio-{self.portfolio_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Hypothesis Portfolio: {self.topic}",
            created_by="TulingResearch Plus hypothesis",
            content=self.model_dump(mode="json"),
            evidence=[
                evidence
                for hypothesis in self.selected
                for evidence in hypothesis.evidence_refs
            ],
            tags=["hypothesis_formation", "portfolio"],
        )

