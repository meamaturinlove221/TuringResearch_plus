"""Experiment Execution workflow models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.hypothesis.models import Hypothesis


class ComputeBudget(BaseModel):
    """Compute budget boundary for an experiment."""

    model_config = ConfigDict(extra="forbid")

    max_runtime_minutes: int = Field(gt=0)
    max_cost_units: float = Field(ge=0.0)
    resource_class: str = Field(min_length=1)


class StatisticalComparisonPlan(BaseModel):
    """Statistical comparison plan."""

    model_config = ConfigDict(extra="forbid")

    primary_test: str = Field(min_length=1)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)
    correction: str = Field(default="none", min_length=1)
    effect_size_metric: str = Field(min_length=1)


class ExperimentPlan(BaseModel):
    """Validated experiment plan generated from a hypothesis."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    hypothesis: Hypothesis
    variables: dict[str, list[str]] = Field(min_length=1)
    controls: list[str] = Field(min_length=1)
    datasets: list[str] = Field(min_length=1)
    metrics: list[str] = Field(min_length=1)
    baselines: list[str] = Field(min_length=1)
    ablations: list[str] = Field(min_length=1)
    expected_outcomes: list[str] = Field(min_length=1)
    failure_modes: list[str] = Field(min_length=1)
    compute_budget: ComputeBudget
    implementation_steps: list[str] = Field(min_length=1)
    reproducibility_checklist: list[str] = Field(min_length=1)
    statistical_comparison_plan: StatisticalComparisonPlan
    evidence_refs: list[EvidenceRef] = Field(min_length=1)

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert the plan to a ResearchArtifact."""

        return ResearchArtifact(
            artifact_id=f"experiment-plan-{self.plan_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Experiment Plan: {self.hypothesis.hypothesis_id}",
            created_by="TuringResearch Plus experiment",
            content=self.model_dump(mode="json"),
            evidence=self.evidence_refs,
            tags=["experiment_execution", "experiment_plan"],
        )


class ConstraintAnalysis(BaseModel):
    """Constraint analysis for an experiment plan."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    constraints: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    mitigation_options: list[str] = Field(default_factory=list)
    feasible: bool


class ScenarioPlan(BaseModel):
    """Scenario plan for experiment execution."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    best_case: str = Field(min_length=1)
    expected_case: str = Field(min_length=1)
    worst_case: str = Field(min_length=1)
    fallback_actions: list[str] = Field(min_length=1)


class ImplementationPlan(BaseModel):
    """Implementation plan for running an experiment."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    steps: list[str] = Field(min_length=1)
    artifacts_to_create: list[str] = Field(min_length=1)
    dry_run: bool = True
    owner: str = Field(default="TuringResearch Plus")


class ResultSchemaField(BaseModel):
    """One result schema field."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    field_type: str = Field(min_length=1)
    required: bool = True
    description: str = Field(min_length=1)


class ResultSchema(BaseModel):
    """Experiment result schema."""

    model_config = ConfigDict(extra="forbid")

    schema_id: str = Field(min_length=1)
    plan_id: str = Field(min_length=1)
    fields: list[ResultSchemaField] = Field(min_length=1)


class ExperimentResultAnalysis(BaseModel):
    """Dry-run result analysis."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    result_schema_id: str = Field(min_length=1)
    metrics_observed: dict[str, float] = Field(default_factory=dict)
    conclusion: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)
    raw_result: dict[str, Any] = Field(default_factory=dict)
