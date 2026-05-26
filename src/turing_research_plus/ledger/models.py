"""State ledger models for workflow state tracking."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from tuling_research_plus.artifacts.models import EvidenceRef, ResearchArtifact


class LedgerEventType(StrEnum):
    """State transition event types."""

    CREATED = "created"
    UPDATED = "updated"
    ARTIFACT = "artifact"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


class LedgerEvent(BaseModel):
    """One state ledger event."""

    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1)
    event_type: LedgerEventType
    message: str = Field(min_length=1)
    evidence: list[EvidenceRef] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class StateLedger(BaseModel):
    """Workflow state ledger."""

    model_config = ConfigDict(extra="forbid")

    ledger_id: str = Field(min_length=1)
    lane: str = Field(min_length=1)
    events: list[LedgerEvent] = Field(default_factory=list)
    artifacts: list[ResearchArtifact] = Field(default_factory=list)
    blockers: list[LedgerEvent] = Field(default_factory=list)

    def append_event(self, event: LedgerEvent) -> "StateLedger":
        """Append an event to this ledger."""

        self.events.append(event)
        return self

    def append_artifact(self, artifact: ResearchArtifact) -> "StateLedger":
        """Append an artifact to this ledger."""

        self.artifacts.append(artifact)
        return self

    def append_blocker(self, event: LedgerEvent) -> "StateLedger":
        """Append a blocker event to this ledger."""

        self.events.append(event)
        self.blockers.append(event)
        return self
