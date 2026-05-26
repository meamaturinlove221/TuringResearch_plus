"""Budget gate models for workflow boundaries."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class BudgetUnit(StrEnum):
    """Units supported by BudgetGate."""

    TOKENS = "tokens"
    SECONDS = "seconds"
    USD = "usd"
    REQUESTS = "requests"


class BudgetGateStatus(StrEnum):
    """Budget gate decision state."""

    OPEN = "open"
    WARN = "warn"
    BLOCKED = "blocked"


class BudgetLimit(BaseModel):
    """Configured budget limit."""

    model_config = ConfigDict(extra="forbid")

    unit: BudgetUnit
    limit: float = Field(gt=0)


class BudgetUsage(BaseModel):
    """Observed budget usage."""

    model_config = ConfigDict(extra="forbid")

    unit: BudgetUnit
    used: float = Field(ge=0)


class BudgetGate(BaseModel):
    """Budget gate required by TulingResearch Plus workflows."""

    model_config = ConfigDict(extra="forbid")

    gate_id: str = Field(min_length=1)
    target: float | None = Field(default=None, gt=0)
    current: float = Field(default=0, ge=0)
    minimum_ratio: float = Field(default=0.0, ge=0.0, le=1.0)
    deviation_reason: str | None = None
    limits: list[BudgetLimit] = Field(min_length=1)
    usage: list[BudgetUsage] = Field(default_factory=list)
    status: BudgetGateStatus = BudgetGateStatus.OPEN
    dry_run_allowed: bool = True

    @property
    def is_blocked(self) -> bool:
        """Return whether this gate blocks workflow execution."""

        return self.status == BudgetGateStatus.BLOCKED

    @property
    def ratio(self) -> float | None:
        """Return current progress against target when a target exists."""

        if self.target is None:
            return None
        return self.current / self.target

    @property
    def meets_minimum_ratio(self) -> bool:
        """Return whether the gate meets its minimum ratio requirement."""

        ratio = self.ratio
        if ratio is None:
            return True
        return ratio >= self.minimum_ratio
