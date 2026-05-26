"""StateLedger append helpers."""

from __future__ import annotations

from uuid import uuid4

from tuling_research_plus.artifacts.models import ResearchArtifact
from tuling_research_plus.ledger.models import LedgerEvent, LedgerEventType, StateLedger


def append_event(ledger: StateLedger, event: LedgerEvent) -> StateLedger:
    """Append an event to a StateLedger."""

    ledger.events.append(event)
    return ledger


def append_artifact(ledger: StateLedger, artifact: ResearchArtifact) -> StateLedger:
    """Append an artifact and record the ledger event."""

    ledger.artifacts.append(artifact)
    ledger.events.append(
        LedgerEvent(
            event_id=f"event-{uuid4()}",
            event_type=LedgerEventType.ARTIFACT,
            message=f"Artifact appended: {artifact.artifact_id}",
            evidence=artifact.evidence,
            metadata={"artifact_id": artifact.artifact_id, "kind": artifact.kind},
        )
    )
    return ledger


def append_blocker(ledger: StateLedger, message: str, event_id: str | None = None) -> StateLedger:
    """Append a blocker event to a StateLedger."""

    event = LedgerEvent(
        event_id=event_id or f"blocker-{uuid4()}",
        event_type=LedgerEventType.BLOCKED,
        message=message,
    )
    ledger.events.append(event)
    ledger.blockers.append(event)
    return ledger
