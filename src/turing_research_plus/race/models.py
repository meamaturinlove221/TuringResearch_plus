"""Race Mode models."""

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from tuling_research_plus.artifacts.models import EvidenceRef


class SourceHygieneStatus(StrEnum):
    """Source hygiene gate status."""

    PASSED = "passed"
    BLOCKED = "blocked"


class IdeaPriority(StrEnum):
    """Race idea priority."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    WATCH = "watch"


class RecommendedAction(StrEnum):
    """Recommended action for an idea."""

    IMPLEMENT = "implement"
    WATCH = "watch"
    DOCUMENT = "document"


class SourceHygieneGate(BaseModel):
    """Gate that protects Race Mode from unauthorized sources."""

    model_config = ConfigDict(extra="forbid")

    status: SourceHygieneStatus
    checked_sources: list[EvidenceRef] = Field(default_factory=list)
    blocked_reason: str | None = None

    @model_validator(mode="after")
    def validate_gate(self) -> Self:
        if self.status == SourceHygieneStatus.PASSED and not self.checked_sources:
            msg = "passed SourceHygieneGate requires at least one checked source"
            raise ValueError(msg)
        if self.status == SourceHygieneStatus.BLOCKED and not self.blocked_reason:
            msg = "blocked SourceHygieneGate requires blocked_reason"
            raise ValueError(msg)
        return self


class IdeaCard(BaseModel):
    """Race Mode idea card."""

    model_config = ConfigDict(extra="forbid")

    idea_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    raw_text: str = ""
    normalized_summary: str = ""
    inferred_intent: str = ""
    source: str = ""
    value_score: float = Field(default=0.0, ge=0.0, le=1.0)
    feasibility_score: float = Field(default=0.0, ge=0.0, le=1.0)
    urgency_score: float = Field(default=0.0, ge=0.0, le=1.0)
    novelty_score: float = Field(default=0.0, ge=0.0, le=1.0)
    priority: IdeaPriority = IdeaPriority.WATCH
    recommended_action: RecommendedAction = RecommendedAction.WATCH
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    uncertain_terms: list[str] = Field(default_factory=list)
    hypothesis: str = ""
    evidence: list[EvidenceRef] = Field(default_factory=list)
    hygiene_gate: SourceHygieneGate
    tags: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def normalize_and_check_hygiene_gate(self) -> Self:
        if not self.raw_text:
            object.__setattr__(self, "raw_text", self.hypothesis or self.title)
        if not self.normalized_summary:
            object.__setattr__(self, "normalized_summary", self.hypothesis or self.title)
        if not self.inferred_intent:
            object.__setattr__(self, "inferred_intent", self.hypothesis or self.title)
        if not self.source:
            object.__setattr__(self, "source", self.idea_id)
        refs = self.evidence_refs or self.evidence
        if refs:
            object.__setattr__(self, "evidence_refs", refs)
            object.__setattr__(self, "evidence", refs)
        if not self.evidence_refs:
            msg = "IdeaCard requires evidence_refs"
            raise ValueError(msg)
        if (
            self.hygiene_gate.status != SourceHygieneStatus.PASSED
            and self.recommended_action == RecommendedAction.IMPLEMENT
        ):
            msg = "IdeaCard implementation requires a passed SourceHygieneGate"
            raise ValueError(msg)
        return self


class FeatureCapsule(BaseModel):
    """Race Mode feature capsule."""

    model_config = ConfigDict(extra="forbid")

    feature_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    idea_cards: list[str] = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    hygiene_gate: SourceHygieneGate

    @model_validator(mode="after")
    def require_passed_hygiene_gate(self) -> Self:
        if self.hygiene_gate.status != SourceHygieneStatus.PASSED:
            msg = "FeatureCapsule requires a passed SourceHygieneGate"
            raise ValueError(msg)
        return self
