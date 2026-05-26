"""Models for optional Apify live adapter."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.adapters.errors import AdapterError


class ApifyRunStatus(StrEnum):
    """Stable Apify run statuses used by fake and live adapters."""

    DRY_RUN = "dry-run"
    LIVE_DISABLED = "live-disabled"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    MISSING_TOKEN = "missing-token"
    ERROR = "error"


class ApifyRunRequest(BaseModel):
    """Input for optional Apify actor run."""

    model_config = ConfigDict(extra="forbid")

    actor_id: str | None = None
    input: dict[str, object] = Field(default_factory=dict)
    dry_run: bool = True
    live_enabled: bool = False
    timeout_seconds: float = Field(default=30.0, gt=0)


class ApifyRunResult(BaseModel):
    """Output for optional Apify actor run."""

    model_config = ConfigDict(extra="forbid")

    actor_id: str | None = None
    run_id: str | None = None
    status: ApifyRunStatus
    input: dict[str, object] = Field(default_factory=dict)
    output_items: list[dict[str, object]] = Field(default_factory=list)
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    warnings: list[str] = Field(default_factory=list)
    errors: list[AdapterError] = Field(default_factory=list)
    requires_human_review: bool = True
