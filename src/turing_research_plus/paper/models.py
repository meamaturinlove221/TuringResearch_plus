"""Paper pipeline boundary models."""

from enum import StrEnum
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import EvidenceRef


class ArticleSection(StrEnum):
    """Supported article sections."""

    ABSTRACT = "abstract"
    INTRODUCTION = "introduction"
    METHODS = "methods"
    RESULTS = "results"
    DISCUSSION = "discussion"
    CONCLUSION = "conclusion"


class ArticleBlockKind(StrEnum):
    """DocFlow article block kinds."""

    RESEARCH_BRIEF = "research_brief"
    RELATED_WORK = "related_work"
    METHOD_DESIGN = "method_design"
    EXPERIMENTS = "experiments"
    PAPER_DRAFT = "paper_draft"


class ArticleBlockStatus(StrEnum):
    """Computed readiness status for one article block."""

    READY = "ready"
    BLOCKED = "blocked"


class DraftStatus(StrEnum):
    """Paper draft request status."""

    PLANNED = "planned"
    BLOCKED = "blocked"


class ExperimentReport(BaseModel):
    """Experiment report required before paper drafting."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    metrics: dict[str, Any] = Field(default_factory=dict)
    evidence: list[EvidenceRef] = Field(min_length=1)


class ArticleBlock(BaseModel):
    """Evidence-backed article text block."""

    model_config = ConfigDict(extra="forbid")

    block_id: str = Field(min_length=1)
    section: ArticleSection
    text: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    block_kind: ArticleBlockKind | None = None
    required_figures: list[str] = Field(default_factory=list)


class PaperDraftRequest(BaseModel):
    """Draft request that blocks when no ExperimentReport is present."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    draft_id: str = Field(min_length=1)
    experiment_report: ExperimentReport | None
    dry_run: bool = True
    status: DraftStatus = DraftStatus.PLANNED
    blocked_reason: str | None = None

    @model_validator(mode="after")
    def block_without_experiment_report(self) -> Self:
        if self.experiment_report is None:
            object.__setattr__(self, "status", DraftStatus.BLOCKED)
            object.__setattr__(
                self,
                "blocked_reason",
                "ExperimentReport is required before Paper Draft",
            )
        return self


class ArticleBlockState(BaseModel):
    """Computed DocFlow state for one article block."""

    model_config = ConfigDict(extra="forbid")

    block_kind: ArticleBlockKind
    title: str = Field(min_length=1)
    path: str = Field(min_length=1)
    required_artifacts: list[str] = Field(default_factory=list)
    present_artifacts: list[str] = Field(default_factory=list)
    missing_artifacts: list[str] = Field(default_factory=list)
    required_figures: list[str] = Field(default_factory=list)
    available_figures: list[str] = Field(default_factory=list)
    missing_figures: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    text: str = ""
    status: ArticleBlockStatus
    blocked_reason: str | None = None

    @property
    def ready(self) -> bool:
        """Return whether this article block is ready."""

        return self.status == ArticleBlockStatus.READY


class ArticleBlockRegistry(BaseModel):
    """Registry of all DocFlow article blocks."""

    model_config = ConfigDict(extra="forbid")

    blocks: list[ArticleBlockState] = Field(min_length=1)
    continuity_graph: str = Field(min_length=1)

    def get_block(self, block_kind: ArticleBlockKind) -> ArticleBlockState:
        """Return a block state by kind."""

        for block in self.blocks:
            if block.block_kind == block_kind:
                return block
        raise KeyError(block_kind)


class MissingEvidenceItem(BaseModel):
    """One missing evidence requirement."""

    model_config = ConfigDict(extra="forbid")

    block_kind: ArticleBlockKind
    requirement: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class MissingItemReport(BaseModel):
    """Missing artifacts, figures, evidence, and blockers."""

    model_config = ConfigDict(extra="forbid")

    missing_artifacts: dict[str, list[str]] = Field(default_factory=dict)
    missing_figures: dict[str, list[str]] = Field(default_factory=dict)
    missing_evidence: list[MissingEvidenceItem] = Field(default_factory=list)
    blockers: dict[str, str] = Field(default_factory=dict)


class PaperReadinessReport(BaseModel):
    """Overall paper readiness report."""

    model_config = ConfigDict(extra="forbid")

    ready: bool
    draft_blocked: bool
    ready_blocks: list[str] = Field(default_factory=list)
    blocked_blocks: list[str] = Field(default_factory=list)
    missing_item_report: MissingItemReport


class DocflowStatusInput(BaseModel):
    """Input for paper.docflow_status and paper.missing_evidence."""

    model_config = ConfigDict(extra="forbid")

    available_artifacts: list[str] = Field(default_factory=list)
    evidence_by_block: dict[str, list[EvidenceRef]] = Field(default_factory=dict)
    required_figures: dict[str, list[str]] = Field(default_factory=dict)
    available_figures: list[str] = Field(default_factory=list)
    block_text: dict[str, str] = Field(default_factory=dict)
    experiment_report: ExperimentReport | None = None


class DocflowStatusOutput(BaseModel):
    """Output for paper.docflow_status."""

    model_config = ConfigDict(extra="forbid")

    registry: ArticleBlockRegistry
    continuity_graph: str = Field(min_length=1)
    missing_item_report: MissingItemReport
    readiness_report: PaperReadinessReport


class ArticleBlockUpdateInput(BaseModel):
    """Input for paper.article_block_update."""

    model_config = ConfigDict(extra="forbid")

    block_kind: ArticleBlockKind
    text: str = Field(min_length=1)
    available_artifacts: list[str] = Field(default_factory=list)
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)
    required_figures: list[str] = Field(default_factory=list)
    available_figures: list[str] = Field(default_factory=list)
    experiment_report: ExperimentReport | None = None


class ArticleBlockUpdateOutput(BaseModel):
    """Output for paper.article_block_update."""

    model_config = ConfigDict(extra="forbid")

    block: ArticleBlockState
    accepted: bool
    missing_evidence: list[MissingEvidenceItem] = Field(default_factory=list)
