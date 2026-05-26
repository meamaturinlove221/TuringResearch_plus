from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.context.index import load_index
from turing_research_plus.context.service import ContextService
from turing_research_plus.context.tools import (
    context_checkpoint,
    context_index,
    context_init,
    context_recover,
    context_summarize,
)


def artifact() -> ResearchArtifact:
    return ResearchArtifact(
        artifact_id="artifact-1",
        kind=ArtifactKind.NOTE,
        title="Indexed Artifact",
        created_by="unit-test",
        evidence=[EvidenceRef(source_id="source-1", locator="p.1", quote="Evidence.")],
    )


def test_index_updates_on_init_and_checkpoint(tmp_path) -> None:
    service = ContextService(tmp_path)

    service.init("campaign-1", "run-1")
    service.checkpoint(
        "campaign-1",
        "run-1",
        label="strategy",
        summary="Indexed summary.",
        artifacts=[artifact()],
    )

    index = load_index(tmp_path)

    assert len(index.entries) == 1
    assert index.entries[0].latest_summary == "Indexed summary."
    assert index.entries[0].artifact_ids == ["artifact-1"]


def test_context_tool_wrappers(tmp_path) -> None:
    init = context_init(tmp_path, "campaign-1", "run-1")
    checkpoint = context_checkpoint(
        tmp_path,
        "campaign-1",
        "run-1",
        "strategy",
        "Tool summary.",
        [artifact()],
    )
    index = context_index(tmp_path)
    recovered = context_recover(tmp_path, "campaign-1", "run-1")
    summary = context_summarize(tmp_path, "campaign-1", "run-1")

    assert init["campaign_id"] == "campaign-1"
    assert checkpoint["summary"] == "Tool summary."
    assert index["entries"][0]["latest_summary"] == "Tool summary."
    assert recovered["latest_summary"] == "Tool summary."
    assert summary["artifact_ids"] == ["artifact-1"]
