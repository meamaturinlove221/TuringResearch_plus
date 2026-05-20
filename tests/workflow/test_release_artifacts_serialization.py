import json

from tuling_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from tuling_research_plus.campaign.models import CampaignResult, WorkflowStatus
from tuling_research_plus.ledger.models import StateLedger


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="source-1", locator="section-1", quote="Evidence.")


def artifact() -> ResearchArtifact:
    return ResearchArtifact(
        artifact_id="artifact-1",
        kind=ArtifactKind.NOTE,
        title="Release Artifact",
        created_by="release-test",
        evidence=[evidence()],
    )


def test_artifacts_serialize_to_markdown_and_json() -> None:
    result = CampaignResult(
        campaign_id="campaign-1",
        run_id="run-1",
        status=WorkflowStatus.COMPLETED,
        artifacts=[artifact()],
        ledger=StateLedger(ledger_id="ledger-1", lane="lane-09"),
    )

    markdown = result.to_markdown()
    payload = result.model_dump(mode="json")
    encoded = json.dumps(payload)

    assert "## Artifacts" in markdown
    assert "`artifact-1`" in markdown
    assert "artifact-1" in encoded
