from __future__ import annotations

from pathlib import Path

from turing_research_plus.remote_readers.fake_reader import (
    FakeRemoteArtifactReader,
    load_remote_fixture_index,
)

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "remote_reader_fixture"
    / "artifact_index.json"
)


def test_fake_reader_returns_vggt_shaped_artifacts() -> None:
    reader = FakeRemoteArtifactReader()

    artifacts = reader.list_artifacts("/remote/vggt/review_bundle")

    assert any(item.path.endswith("review/final_status.json") for item in artifacts)
    assert any(item.path.endswith("large/predictions.npz") for item in artifacts)
    assert any(item.is_symlink for item in artifacts)


def test_fixture_loader_reads_local_index_without_network() -> None:
    artifacts = load_remote_fixture_index(FIXTURE)

    assert any(item.path.endswith("review/failure_report.md") for item in artifacts)
    assert any(item.path.endswith(".env") for item in artifacts)
