"""Context management models for TulingResearch Plus."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from tuling_research_plus.artifacts.models import EvidenceRef, ResearchArtifact


class ContextSession(BaseModel):
    """One campaign run context file."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    context_path: Path
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = Field(default_factory=dict)


class ContextCheckpoint(BaseModel):
    """Append-only checkpoint for a strategy or workflow state."""

    model_config = ConfigDict(extra="forbid")

    checkpoint_id: str = Field(min_length=1)
    campaign_id: str = Field(min_length=1)
    run_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    summary: str = Field(min_length=1)
    artifacts: list[ResearchArtifact] = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    state: dict[str, Any] = Field(default_factory=dict)


class ContextIndexEntry(BaseModel):
    """Index entry for one context file."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str
    run_id: str
    context_path: Path
    latest_checkpoint_id: str | None = None
    latest_summary: str | None = None
    artifact_ids: list[str] = Field(default_factory=list)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ContextIndex(BaseModel):
    """Context index file."""

    model_config = ConfigDict(extra="forbid")

    entries: list[ContextIndexEntry] = Field(default_factory=list)


class ContextRecoverResult(BaseModel):
    """Recover result for the latest run state."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str
    run_id: str
    latest_summary: str
    artifacts: list[ResearchArtifact] = Field(default_factory=list)
    evidence: list[EvidenceRef] = Field(default_factory=list)
    checkpoint: ContextCheckpoint | None = None


class ContextSummary(BaseModel):
    """Compact context summary."""

    model_config = ConfigDict(extra="forbid")

    campaign_id: str
    run_id: str
    checkpoint_count: int = Field(ge=0)
    latest_summary: str | None = None
    artifact_ids: list[str] = Field(default_factory=list)
