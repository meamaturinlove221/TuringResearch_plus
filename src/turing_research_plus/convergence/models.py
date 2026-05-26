"""Convergence workflow models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tuling_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


class CandidateKind(StrEnum):
    """Supported convergence candidate kinds."""

    IDEA = "idea"
    HYPOTHESIS = "hypothesis"
    EXPERIMENT = "experiment"
    IMPLEMENTATION_VARIANT = "implementation_variant"
    PAPER_DIRECTION = "paper_direction"
    RELEASE_FEATURE = "release_feature"


class PromotionDecision(StrEnum):
    """Promotion decision outcomes."""

    PROMOTE = "promote"
    REJECT = "reject"
    HOLD = "hold"


class ConvergenceCandidate(BaseModel):
    """Normalized candidate for convergence decisions."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    kind: CandidateKind
    title: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    expected_gain: str = Field(min_length=1)
    feasibility: float = Field(ge=0.0, le=1.0)
    novelty: float = Field(ge=0.0, le=1.0)
    risk: str = Field(min_length=1)
    required_resources: list[str] = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)
    metadata: dict[str, Any] = Field(default_factory=dict)


class CandidateScore(BaseModel):
    """Scored candidate."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    total_score: float = Field(ge=0.0, le=1.0)
    criteria: dict[str, float] = Field(min_length=1)
    rationale: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)


class FeasibilityAssessment(BaseModel):
    """Feasibility assessment for one candidate."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    feasible: bool
    score: float = Field(ge=0.0, le=1.0)
    notes: list[str] = Field(min_length=1)
    blockers: list[str] = Field(default_factory=list)


class PairwisePreference(BaseModel):
    """Pairwise comparison result."""

    model_config = ConfigDict(extra="forbid")

    left_id: str = Field(min_length=1)
    right_id: str = Field(min_length=1)
    winner_id: str = Field(min_length=1)
    margin: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(min_length=1)


class PromotionDecisionResult(BaseModel):
    """Promotion decision for one candidate."""

    model_config = ConfigDict(extra="forbid")

    candidate_id: str = Field(min_length=1)
    decision: PromotionDecision
    reason: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class DecisionReport(BaseModel):
    """Convergence decision report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    ranked_candidates: list[CandidateScore] = Field(min_length=1)
    scoring_matrix: dict[str, dict[str, float]] = Field(min_length=1)
    pairwise_matrix: list[PairwisePreference] | None = None
    sensitivity_analysis: list[str] = Field(min_length=1)
    feasibility_notes: list[FeasibilityAssessment] = Field(min_length=1)
    rejected_candidates: list[CandidateScore] = Field(default_factory=list)
    steelman_for_rejected: dict[str, str] = Field(default_factory=dict)
    final_recommendation: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)
    next_actions: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def ensure_recommendation_is_ranked(self) -> "DecisionReport":
        candidate_ids = {candidate.candidate_id for candidate in self.ranked_candidates}
        if self.final_recommendation not in candidate_ids:
            raise ValueError("final recommendation must reference a ranked candidate")
        return self

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert report to a ResearchArtifact."""

        evidence = [
            evidence
            for score in self.ranked_candidates
            for evidence in score.evidence_refs
        ]
        return ResearchArtifact(
            artifact_id=f"decision-{self.report_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title="Convergence Decision Report",
            created_by="TulingResearch Plus convergence",
            content=self.model_dump(mode="json"),
            evidence=evidence,
            tags=["convergence", "decision_report"],
        )

