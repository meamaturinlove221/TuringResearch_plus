import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.context.models import ContextCheckpoint, ContextSession


def artifact() -> ResearchArtifact:
    return ResearchArtifact(
        artifact_id="artifact-1",
        kind=ArtifactKind.NOTE,
        title="Context artifact",
        created_by="unit-test",
        evidence=[EvidenceRef(source_id="source-1", locator="p.1", quote="Evidence.")],
    )


def test_context_session_model(tmp_path) -> None:
    session = ContextSession(
        campaign_id="campaign-1",
        run_id="run-1",
        context_path=tmp_path / "context.jsonl",
    )

    assert session.campaign_id == "campaign-1"
    assert session.context_path.name == "context.jsonl"


def test_checkpoint_requires_artifact_links() -> None:
    with pytest.raises(ValidationError):
        ContextCheckpoint(
            checkpoint_id="checkpoint-1",
            campaign_id="campaign-1",
            run_id="run-1",
            label="strategy-complete",
            summary="Done.",
            artifacts=[],
            evidence=[EvidenceRef(source_id="source-1", locator="p.1", quote="Evidence.")],
        )


def test_checkpoint_preserves_evidence_links() -> None:
    checkpoint = ContextCheckpoint(
        checkpoint_id="checkpoint-1",
        campaign_id="campaign-1",
        run_id="run-1",
        label="strategy-complete",
        summary="Strategy completed.",
        artifacts=[artifact()],
        evidence=artifact().evidence,
    )

    assert checkpoint.artifacts[0].artifact_id == "artifact-1"
    assert checkpoint.evidence[0].source_id == "source-1"
