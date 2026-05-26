from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.context.service import ContextService


def artifact(artifact_id: str = "artifact-1") -> ResearchArtifact:
    return ResearchArtifact(
        artifact_id=artifact_id,
        kind=ArtifactKind.NOTE,
        title=f"Artifact {artifact_id}",
        created_by="unit-test",
        evidence=[EvidenceRef(source_id=f"source-{artifact_id}", locator="p.1", quote="Evidence.")],
    )


def test_init_creates_file(tmp_path) -> None:
    session = ContextService(tmp_path).init("campaign-1", "run-1")

    assert session.context_path.exists()
    assert session.context_path.read_text(encoding="utf-8") == ""


def test_checkpoint_appends_and_preserves_artifact_links(tmp_path) -> None:
    service = ContextService(tmp_path)
    service.init("campaign-1", "run-1")

    first = service.checkpoint(
        "campaign-1",
        "run-1",
        label="strategy-1",
        summary="First strategy complete.",
        artifacts=[artifact("artifact-1")],
    )
    second = service.checkpoint(
        "campaign-1",
        "run-1",
        label="strategy-2",
        summary="Second strategy complete.",
        artifacts=[artifact("artifact-2")],
    )

    lines = first.model_dump_json(), second.model_dump_json()
    content = (tmp_path / "campaign-1__run-1.jsonl").read_text(encoding="utf-8")
    assert len(content.splitlines()) == 2
    assert first.checkpoint_id in lines[0]
    assert second.checkpoint_id in lines[1]
    assert second.artifacts[0].artifact_id == "artifact-2"
    assert second.evidence[0].source_id == "source-artifact-2"


def test_recover_latest_state(tmp_path) -> None:
    service = ContextService(tmp_path)
    service.checkpoint(
        "campaign-1",
        "run-1",
        label="strategy-1",
        summary="First state.",
        artifacts=[artifact("artifact-1")],
    )
    service.checkpoint(
        "campaign-1",
        "run-1",
        label="strategy-2",
        summary="Latest state.",
        artifacts=[artifact("artifact-2")],
    )

    recovered = service.recover("campaign-1", "run-1")

    assert recovered.latest_summary == "Latest state."
    assert [item.artifact_id for item in recovered.artifacts] == ["artifact-2"]
    assert recovered.evidence[0].source_id == "source-artifact-2"


def test_summarize_returns_checkpoint_count_and_artifacts(tmp_path) -> None:
    service = ContextService(tmp_path)
    service.checkpoint(
        "campaign-1",
        "run-1",
        label="strategy-1",
        summary="First state.",
        artifacts=[artifact("artifact-1")],
    )

    summary = service.summarize("campaign-1", "run-1")

    assert summary.checkpoint_count == 1
    assert summary.artifact_ids == ["artifact-1"]
