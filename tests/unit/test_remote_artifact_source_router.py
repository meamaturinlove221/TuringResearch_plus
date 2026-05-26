from __future__ import annotations

from pathlib import Path

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import GitHubArtifactSyncRequest
from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.models import ObjectArtifactIndexRequest
from turing_research_plus.remote_artifacts.models import (
    RemoteArtifactSourceKind,
    RemoteArtifactStatus,
)
from turing_research_plus.remote_artifacts.source_router import (
    artifacts_from_github,
    artifacts_from_object_store,
    source_from_github,
    source_from_object_store,
)

GITHUB_FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "github_artifact_sync_fixture"
    / "artifact_index.json"
)


def test_source_router_normalizes_github_report() -> None:
    report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/vggt-review-artifacts",
            source_ref="main",
            fixture_index_path=GITHUB_FIXTURE,
        )
    )

    source = source_from_github(report)
    artifacts = artifacts_from_github(report)

    assert source.kind == RemoteArtifactSourceKind.GITHUB
    assert any(item.status == RemoteArtifactStatus.SELECTED for item in artifacts)
    assert any(item.status == RemoteArtifactStatus.METADATA_ONLY for item in artifacts)
    assert any(item.status == RemoteArtifactStatus.UNSAFE for item in artifacts)


def test_source_router_normalizes_object_index() -> None:
    index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            bucket_or_container="vggt-review-artifacts",
            prefix="modal-sparseconv-review",
        )
    )

    source = source_from_object_store(index)
    artifacts = artifacts_from_object_store(index)

    assert source.kind == RemoteArtifactSourceKind.CLOUD_OBJECT
    assert any(item.path.endswith("review/final_status.json") for item in artifacts)
