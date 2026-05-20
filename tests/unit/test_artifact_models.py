import pytest
from pydantic import ValidationError

from tuling_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="src-1", locator="p.1", quote="Public evidence.")


def test_research_artifact_requires_evidence() -> None:
    artifact = ResearchArtifact(
        artifact_id="artifact-1",
        kind=ArtifactKind.NOTE,
        title="Evidence backed note",
        created_by="unit-test",
        evidence=[evidence()],
    )

    assert artifact.kind == ArtifactKind.NOTE
    assert artifact.evidence[0].source_id == "src-1"


def test_research_artifact_rejects_empty_evidence() -> None:
    with pytest.raises(ValidationError):
        ResearchArtifact(
            artifact_id="artifact-1",
            kind=ArtifactKind.NOTE,
            title="No evidence",
            created_by="unit-test",
            evidence=[],
        )
