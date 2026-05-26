"""Campaign and workflow run boundary models."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.artifacts.models import ResearchArtifact
from turing_research_plus.budget.models import BudgetGate
from turing_research_plus.ledger.models import LedgerEvent, StateLedger


class CampaignMode(StrEnum):
    """Execution mode for workflow skeletons."""

    DRY_RUN = "dry_run"
    FAKE_SERVICE = "fake_service"
    LIVE = "live"


class WorkflowStatus(StrEnum):
    """Shared workflow status values."""

    PLANNED = "planned"
    RUNNING = "running"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


class SOPExecutionMode(StrEnum):
    """Supported SOP execution modes."""

    DIRECT = "direct"
    IMPORTED = "imported"
    SUBTASK = "subtask"


class QualityGateSpec(BaseModel):
    """Named quality gate required by a campaign."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    description: str = Field(min_length=1)
    required: bool = True


class SOPSpec(BaseModel):
    """Executable SOP unit."""

    model_config = ConfigDict(extra="forbid")

    sop_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    execution_mode: SOPExecutionMode = SOPExecutionMode.DIRECT
    handler: str = Field(default="default", min_length=1)
    inputs: dict[str, Any] = Field(default_factory=dict)


class TacticSpec(BaseModel):
    """Tactic containing ordered SOPs."""

    model_config = ConfigDict(extra="forbid")

    tactic_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    sops: list[SOPSpec] = Field(default_factory=list)


class StrategySpec(BaseModel):
    """Campaign strategy containing ordered tactics."""

    model_config = ConfigDict(extra="forbid")

    strategy_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    tactics: list[TacticSpec] = Field(default_factory=list)
    selection_tags: list[str] = Field(default_factory=list)


class CampaignSpec(BaseModel):
    """Top-level workflow campaign specification."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    mode: CampaignMode = CampaignMode.DRY_RUN
    budget_gate: BudgetGate
    state_ledger: StateLedger
    strategies: list[StrategySpec] = Field(default_factory=list)
    quality_gates: list[QualityGateSpec] = Field(default_factory=list)
    inputs: dict[str, Any] = Field(default_factory=dict)
    required_services: list[str] = Field(default_factory=list)
    status: WorkflowStatus = WorkflowStatus.PLANNED

    @model_validator(mode="after")
    def require_unique_strategy_ids(self) -> "CampaignSpec":
        strategy_ids = [strategy.strategy_id for strategy in self.strategies]
        if len(strategy_ids) != len(set(strategy_ids)):
            msg = "strategy IDs must be unique"
            raise ValueError(msg)
        return self

    @property
    def dry_run(self) -> bool:
        """Return whether this campaign is running in dry-run mode."""

        return self.mode == CampaignMode.DRY_RUN

    @property
    def fake_service(self) -> bool:
        """Return whether this campaign uses fake service boundaries."""

        return self.mode == CampaignMode.FAKE_SERVICE


class CampaignRun(BaseModel):
    """Runtime state for a campaign execution."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(min_length=1)
    campaign_id: str = Field(min_length=1)
    selected_strategy_id: str | None = None
    status: WorkflowStatus = WorkflowStatus.PLANNED
    ledger: StateLedger
    artifacts: list[ResearchArtifact] = Field(default_factory=list)
    events: list[LedgerEvent] = Field(default_factory=list)


class CampaignResult(BaseModel):
    """Result returned by CampaignRunner."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    status: WorkflowStatus
    selected_strategy_id: str | None = None
    artifacts: list[ResearchArtifact] = Field(default_factory=list)
    ledger: StateLedger
    quality_gate_results: dict[str, bool] = Field(default_factory=dict)
    blocked_reason: str | None = None

    def to_markdown(self) -> str:
        """Serialize the result as a compact Markdown report."""

        lines = [
            f"# Campaign Result: {self.campaign_id}",
            "",
            f"- Run ID: `{self.run_id}`",
            f"- Status: `{self.status}`",
            f"- Selected strategy: `{self.selected_strategy_id or 'none'}`",
            f"- Artifacts: {len(self.artifacts)}",
        ]
        if self.blocked_reason:
            lines.append(f"- Blocked reason: {self.blocked_reason}")
        if self.quality_gate_results:
            lines.extend(["", "## Quality Gates"])
            for gate_id, passed in self.quality_gate_results.items():
                status = "passed" if passed else "failed"
                lines.append(f"- `{gate_id}`: {status}")
        if self.artifacts:
            lines.extend(["", "## Artifacts"])
            for artifact in self.artifacts:
                lines.append(f"- `{artifact.artifact_id}`: {artifact.title}")
        return "\n".join(lines) + "\n"
