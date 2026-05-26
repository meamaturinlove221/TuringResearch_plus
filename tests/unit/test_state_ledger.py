from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.ledger.models import LedgerEvent, LedgerEventType, StateLedger
from turing_research_plus.ledger.state_ledger import append_artifact, append_blocker, append_event


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="source-1", locator="p.1", quote="Evidence.")


def artifact() -> ResearchArtifact:
    return ResearchArtifact(
        artifact_id="artifact-1",
        kind=ArtifactKind.NOTE,
        title="Ledger artifact",
        created_by="unit-test",
        evidence=[evidence()],
    )


def test_state_ledger_model_appends_event_artifact_and_blocker() -> None:
    ledger = StateLedger(ledger_id="ledger-1", lane="lane-06")
    event = LedgerEvent(
        event_id="event-1",
        event_type=LedgerEventType.UPDATED,
        message="State updated.",
    )
    blocker = LedgerEvent(
        event_id="blocker-1",
        event_type=LedgerEventType.BLOCKED,
        message="Blocked on contract.",
    )

    ledger.append_event(event)
    ledger.append_artifact(artifact())
    ledger.append_blocker(blocker)

    assert ledger.events == [event, blocker]
    assert ledger.artifacts[0].artifact_id == "artifact-1"
    assert ledger.blockers == [blocker]


def test_state_ledger_helper_appends_event_artifact_and_blocker() -> None:
    ledger = StateLedger(ledger_id="ledger-2", lane="lane-06")
    event = LedgerEvent(
        event_id="event-2",
        event_type=LedgerEventType.CREATED,
        message="Created ledger.",
    )

    append_event(ledger, event)
    append_artifact(ledger, artifact())
    append_blocker(ledger, "Waiting for budget approval.", event_id="blocker-2")

    assert ledger.events[0] == event
    assert ledger.events[1].event_type == LedgerEventType.ARTIFACT
    assert ledger.blockers[0].event_id == "blocker-2"
    assert ledger.artifacts[0].artifact_id == "artifact-1"
