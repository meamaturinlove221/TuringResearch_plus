from __future__ import annotations

from pathlib import Path

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import GitHubArtifactSyncRequest
from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.models import ObjectArtifactIndexRequest
from turing_research_plus.remote_artifacts.models import (
    ArtifactRef,
    RemoteArtifactSourceKind,
    RemoteArtifactStatus,
)
from turing_research_plus.remote_artifacts.unified_report import (
    _find_duplicate_candidates,
    build_unified_remote_artifact_report,
)

GITHUB_FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "github_artifact_sync_fixture"
    / "artifact_index.json"
)


def test_unified_report_collects_selected_omitted_and_unsafe_artifacts() -> None:
    github_report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/vggt-review-artifacts",
            source_ref="main",
            fixture_index_path=GITHUB_FIXTURE,
        )
    )
    object_index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            bucket_or_container="vggt-review-artifacts",
            prefix="modal-sparseconv-review",
        )
    )

    report = build_unified_remote_artifact_report(
        github_reports=[github_report],
        object_indexes=[object_index],
    )

    assert len(report.sources) == 2
    assert report.selected_artifacts
    assert report.omitted_artifacts
    assert report.unsafe_artifacts
    assert report.proposed_imports
    assert report.requires_human_review is True
    assert report.human_verified is False


def test_duplicate_candidates_can_be_found_by_sha256() -> None:
    artifacts = [
        ArtifactRef(
            artifact_id="github:a",
            source_id="github:repo:main",
            source_kind=RemoteArtifactSourceKind.GITHUB,
            path="review/final_status.json",
            sha256="a" * 64,
            status=RemoteArtifactStatus.SELECTED,
        ),
        ArtifactRef(
            artifact_id="cloud:a",
            source_id="cloud:bucket:prefix",
            source_kind=RemoteArtifactSourceKind.CLOUD_OBJECT,
            path="review/final_status.json",
            sha256="a" * 64,
            status=RemoteArtifactStatus.SELECTED,
        ),
    ]

    assert _find_duplicate_candidates(artifacts) == [["cloud:a", "github:a"]]
