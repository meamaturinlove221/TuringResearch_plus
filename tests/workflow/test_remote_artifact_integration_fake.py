from __future__ import annotations

from pathlib import Path

from turing_research_plus.github_sync.importer import build_github_artifact_sync_report
from turing_research_plus.github_sync.models import GitHubArtifactSyncRequest
from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.index import load_object_artifact_index
from turing_research_plus.object_store.models import ObjectArtifactIndexRequest
from turing_research_plus.remote_artifacts.models import RemoteArtifactSourceKind
from turing_research_plus.remote_artifacts.unified_report import (
    build_unified_remote_artifact_report,
)
from turing_research_plus.remote_readers.models import RemoteReaderRequest
from turing_research_plus.remote_readers.tools import read_remote_artifacts
from turing_research_plus.shared_store.local_mount_reader import scan_local_mount
from turing_research_plus.shared_store.models import SharedStoreScanRequest

ROOT = Path(__file__).resolve().parents[2]
GITHUB_FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "github_artifact_sync_fixture"
    / "artifact_index.json"
)
REMOTE_FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "remote_reader_fixture"
    / "artifact_index.json"
)
SHARED_FIXTURE = ROOT / "examples" / "vggt-human-prior-survey" / "shared_store_fixture"
OBJECT_FIXTURE = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "object_store_fixture"
    / "artifact_index.json"
)


def test_remote_artifact_integration_fake_unifies_all_sources() -> None:
    github_report = build_github_artifact_sync_report(
        GitHubArtifactSyncRequest(
            source_repo="example/vggt-review-artifacts",
            source_ref="modal-sparseconv-review",
            fixture_index_path=GITHUB_FIXTURE,
        )
    )
    remote_report = read_remote_artifacts(
        RemoteReaderRequest(
            host_label="fake-vggt-remote",
            root_path="/remote/vggt/review_bundle",
            fixture_index_path=REMOTE_FIXTURE,
        )
    )
    shared_report = scan_local_mount(
        SharedStoreScanRequest(
            mount_label="fake-shared-store",
            root_path=SHARED_FIXTURE,
        )
    )
    fixture_index = load_object_artifact_index(OBJECT_FIXTURE)
    object_index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            provider=fixture_index.provider,
            bucket_or_container=fixture_index.bucket_or_container,
            prefix=fixture_index.prefix,
        ),
        objects=fixture_index.objects,
    )

    report = build_unified_remote_artifact_report(
        github_reports=[github_report],
        remote_reader_reports=[remote_report],
        shared_store_reports=[shared_report],
        object_indexes=[object_index],
    )
    markdown = report.to_markdown()

    assert {source.kind for source in report.sources} == {
        RemoteArtifactSourceKind.GITHUB,
        RemoteArtifactSourceKind.SSH_SFTP,
        RemoteArtifactSourceKind.NAS_SMB,
        RemoteArtifactSourceKind.CLOUD_OBJECT,
    }
    assert report.selected_artifacts
    assert report.omitted_artifacts
    assert report.unsafe_artifacts
    assert all(item["status"] == "requires-human-review" for item in report.proposed_imports)
    assert report.human_verified is False
    assert "SparseConv3D" not in markdown
