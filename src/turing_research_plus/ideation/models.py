"""Creative Ideation workflow models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


class IdeaRisk(StrEnum):
    """Risk profile for an idea candidate."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class IdeaClusterKey(BaseModel):
    """Diversity cluster dimensions."""

    model_config = ConfigDict(extra="forbid")

    mechanism: str = Field(min_length=1)
    required_data: str = Field(min_length=1)
    model_component: str = Field(min_length=1)
    evaluation_target: str = Field(min_length=1)
    risk_profile: IdeaRisk

    def signature(self) -> tuple[str, str, str, str, IdeaRisk]:
        """Return a stable cluster signature."""

        return (
            self.mechanism.lower(),
            self.required_data.lower(),
            self.model_component.lower(),
            self.evaluation_target.lower(),
            self.risk_profile,
        )


class IdeaCandidate(BaseModel):
    """Evidence-backed research idea candidate."""

    model_config = ConfigDict(extra="forbid")

    idea_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    hypothesis_link: str = Field(min_length=1)
    mechanism: str = Field(min_length=1)
    novelty: float = Field(ge=0.0, le=1.0)
    feasibility: float = Field(ge=0.0, le=1.0)
    risk: IdeaRisk
    expected_gain: str = Field(min_length=1)
    required_resources: list[str] = Field(min_length=1)
    nearest_existing_work: str = Field(min_length=1)
    why_not_duplicate: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)
    cluster_key: IdeaClusterKey

    @property
    def quality_score(self) -> float:
        """Return a deterministic quality score."""

        risk_penalty = {
            IdeaRisk.LOW: 0.0,
            IdeaRisk.MEDIUM: 0.08,
            IdeaRisk.HIGH: 0.16,
        }[self.risk]
        return round(max(0.0, min(1.0, (self.novelty + self.feasibility) / 2 - risk_penalty)), 3)


class MorphologicalAxis(BaseModel):
    """One morphological matrix axis."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    options: list[str] = Field(min_length=1)


class MorphologicalMatrix(BaseModel):
    """Morphological matrix for ideation."""

    model_config = ConfigDict(extra="forbid")

    matrix_id: str = Field(min_length=1)
    hypothesis_link: str = Field(min_length=1)
    axes: list[MorphologicalAxis] = Field(min_length=1)

    def combinations(self) -> list[dict[str, str]]:
        """Return deterministic one-to-one option combinations."""

        max_len = max(len(axis.options) for axis in self.axes)
        rows: list[dict[str, str]] = []
        for index in range(max_len):
            rows.append(
                {
                    axis.name: axis.options[index % len(axis.options)]
                    for axis in self.axes
                }
            )
        return rows


class IdeaGenerationResult(BaseModel):
    """Generated ideas before filtering."""

    model_config = ConfigDict(extra="forbid")

    result_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    candidates: list[IdeaCandidate] = Field(min_length=1)


class DiversityFilterReport(BaseModel):
    """Quality-diversity filter output."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    retained: list[IdeaCandidate] = Field(default_factory=list)
    rejected_duplicates: list[IdeaCandidate] = Field(default_factory=list)
    cluster_count: int = Field(ge=0)

    @model_validator(mode="after")
    def ensure_unique_retained_clusters(self) -> "DiversityFilterReport":
        signatures = [candidate.cluster_key.signature() for candidate in self.retained]
        if len(signatures) != len(set(signatures)):
            raise ValueError("retained ideas must have unique diversity clusters")
        return self


class IdeaPortfolio(BaseModel):
    """Artifact-shaped ideation output."""

    model_config = ConfigDict(extra="forbid")

    portfolio_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    ideas: list[IdeaCandidate] = Field(min_length=1)
    diversity_report: DiversityFilterReport

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert ideas to a ResearchArtifact."""

        return ResearchArtifact(
            artifact_id=f"idea-portfolio-{self.portfolio_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Idea Portfolio: {self.topic}",
            created_by="TuringResearch Plus ideation",
            content=self.model_dump(mode="json"),
            evidence=[
                evidence
                for idea in self.ideas
                for evidence in idea.evidence_refs
            ],
            tags=["creative_ideation", "quality_diversity"],
        )
