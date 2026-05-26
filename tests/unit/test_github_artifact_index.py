from __future__ import annotations

from pathlib import Path

from turing_research_plus.github_sync.artifact_index import (
    filter_selected_artifacts,
    load_artifact_index,
)

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "github_artifact_sync_fixture"
    / "artifact_index.json"
)


def test_load_artifact_index_fixture() -> None:
    artifacts = load_artifact_index(FIXTURE)

    assert len(artifacts) >= 3
    assert any(artifact.path == "review/final_status.json" for artifact in artifacts)


def test_filter_selected_artifacts_by_pattern() -> None:
    artifacts = load_artifact_index(FIXTURE)
    selected = filter_selected_artifacts(artifacts, ["failure"])

    assert [artifact.path for artifact in selected] == ["review/failure_report.md"]
