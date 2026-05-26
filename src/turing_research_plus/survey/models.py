"""Literature survey models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


class SurveyStrategy(StrEnum):
    """Supported literature survey strategies."""

    SCOPING = "scoping_survey"
    SYSTEMATIC = "systematic_survey"
    DEEP = "deep_survey"
    NARRATIVE = "narrative_review"
    SNOWBALL = "snowball_survey"


class SurveyStatus(StrEnum):
    """Survey execution status."""

    PLANNED = "planned"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"


class SurveyInput(BaseModel):
    """Input for research.survey_plan and research.survey_run."""

    model_config = ConfigDict(extra="forbid")

    topic: str = Field(min_length=1)
    strategy: SurveyStrategy
    year_range: tuple[int, int] | None = None
    min_papers: int = Field(default=5, gt=0)
    full_text_ratio: float = Field(default=0.6, ge=0.0, le=1.0)
    seed_papers: list[str] = Field(default_factory=list)
    research_goal: str = Field(min_length=1)

    @model_validator(mode="after")
    def validate_year_range(self) -> "SurveyInput":
        if self.year_range is not None and self.year_range[0] > self.year_range[1]:
            raise ValueError("year_range start must be <= end")
        return self


class SurveyPlan(BaseModel):
    """Planned literature survey configuration."""

    model_config = ConfigDict(extra="forbid")

    survey_id: str = Field(min_length=1)
    survey_input: SurveyInput
    search_budget: int = Field(gt=0)
    screening_budget: int = Field(gt=0)
    full_text_target: int = Field(ge=0)
    notes: list[str] = Field(default_factory=list)


class PaperRecord(BaseModel):
    """Paper candidate used by survey fake services."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    year: int | None = None
    abstract: str | None = None
    has_full_text: bool = False
    pdf_markdown_path: str | None = None
    evidence: list[EvidenceRef] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)

    @property
    def counts_as_full_text(self) -> bool:
        """Return whether this paper satisfies full-text evidence."""

        return self.has_full_text or self.pdf_markdown_path is not None


class PaperScreeningDecision(StrEnum):
    """Screening decision values."""

    INCLUDE = "include"
    EXCLUDE = "exclude"


class PaperScreeningRow(BaseModel):
    """One row in a paper screening table."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    decision: PaperScreeningDecision
    reason: str = Field(min_length=1)
    full_text_available: bool
    evidence: list[EvidenceRef] = Field(default_factory=list)


class PaperScreeningTable(BaseModel):
    """Screened paper candidates."""

    model_config = ConfigDict(extra="forbid")

    rows: list[PaperScreeningRow] = Field(default_factory=list)

    @property
    def included_count(self) -> int:
        return sum(row.decision == PaperScreeningDecision.INCLUDE for row in self.rows)

    @property
    def full_text_count(self) -> int:
        return sum(
            row.decision == PaperScreeningDecision.INCLUDE and row.full_text_available
            for row in self.rows
        )


class MethodTaxonomy(BaseModel):
    """Simple method taxonomy extracted from included papers."""

    model_config = ConfigDict(extra="forbid")

    methods: dict[str, list[str]] = Field(default_factory=dict)


class EvidenceMatrixRow(BaseModel):
    """Evidence matrix row."""

    model_config = ConfigDict(extra="forbid")

    claim: str = Field(min_length=1)
    paper_ids: list[str] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(min_length=1)


class EvidenceMatrix(BaseModel):
    """Evidence matrix for survey claims."""

    model_config = ConfigDict(extra="forbid")

    rows: list[EvidenceMatrixRow] = Field(default_factory=list)


class GapItem(BaseModel):
    """Evidence-backed research gap."""

    model_config = ConfigDict(extra="forbid")

    gap_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    severity: str = "medium"


class GapList(BaseModel):
    """List of evidence-backed final gaps."""

    model_config = ConfigDict(extra="forbid")

    gaps: list[GapItem] = Field(default_factory=list)


class PRISMAFlow(BaseModel):
    """Minimal PRISMA-like flow counts."""

    model_config = ConfigDict(extra="forbid")

    identified: int = Field(ge=0)
    screened: int = Field(ge=0)
    included: int = Field(ge=0)


class CitationLineage(BaseModel):
    """Snowball lineage summary."""

    model_config = ConfigDict(extra="forbid")

    seed_papers: list[str] = Field(default_factory=list)
    expanded_papers: list[str] = Field(default_factory=list)
    saturation_reached: bool = False


class LiteratureSurveyArtifact(BaseModel):
    """Structured output of a literature survey workflow."""

    model_config = ConfigDict(extra="forbid")

    survey_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    strategy: SurveyStrategy
    status: SurveyStatus
    screening_table: PaperScreeningTable
    method_taxonomy: MethodTaxonomy
    evidence_matrix: EvidenceMatrix
    gap_list: GapList
    prisma_flow: PRISMAFlow | None = None
    citation_lineage: CitationLineage | None = None
    warnings: list[str] = Field(default_factory=list)

    def to_research_artifact(self) -> ResearchArtifact:
        """Convert survey output to a generic ResearchArtifact."""

        evidence = [
            evidence
            for gap in self.gap_list.gaps
            for evidence in gap.evidence
        ]
        if not evidence:
            evidence = [
                evidence
                for row in self.evidence_matrix.rows
                for evidence in row.evidence
            ]
        return ResearchArtifact(
            artifact_id=f"survey-{self.survey_id}",
            kind=ArtifactKind.WORKFLOW_STATE,
            title=f"Literature Survey: {self.topic}",
            created_by="TuringResearch Plus survey",
            content=self.model_dump(mode="json"),
            evidence=evidence,
            tags=["literature_survey", self.strategy],
        )


class SurveyResult(BaseModel):
    """Result returned by survey service."""

    model_config = ConfigDict(extra="forbid")

    status: SurveyStatus
    plan: SurveyPlan
    artifact: LiteratureSurveyArtifact | None = None
    blocked_reason: str | None = None

    def to_markdown(self) -> str:
        """Export a survey result as Markdown."""

        lines = [
            f"# Literature Survey: {self.plan.survey_input.topic}",
            "",
            f"- Strategy: `{self.plan.survey_input.strategy}`",
            f"- Status: `{self.status}`",
        ]
        if self.blocked_reason:
            lines.append(f"- Blocked reason: {self.blocked_reason}")
        if self.artifact is not None:
            lines.extend(["", "## Gaps"])
            for gap in self.artifact.gap_list.gaps:
                lines.append(f"- `{gap.gap_id}`: {gap.description}")
            lines.extend(["", "## Evidence Matrix"])
            for row in self.artifact.evidence_matrix.rows:
                lines.append(f"- {row.claim} ({', '.join(row.paper_ids)})")
        return "\n".join(lines) + "\n"
