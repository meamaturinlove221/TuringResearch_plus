"""Build unified remote artifact reports from source-specific reports."""

from __future__ import annotations

from collections import defaultdict

from turing_research_plus.github_sync.models import GitHubArtifactSyncReport
from turing_research_plus.object_store.models import ObjectArtifactIndex
from turing_research_plus.remote_artifacts.models import (
    ArtifactRef,
    RemoteArtifactStatus,
    UnifiedRemoteArtifactReport,
)
from turing_research_plus.remote_artifacts.safety import duplicate_key
from turing_research_plus.remote_artifacts.source_router import (
    artifacts_from_github,
    artifacts_from_object_store,
    artifacts_from_remote_reader,
    artifacts_from_shared_store,
    source_from_github,
    source_from_object_store,
    source_from_remote_reader,
    source_from_shared_store,
)
from turing_research_plus.remote_readers.models import RemoteReaderReport
from turing_research_plus.shared_store.models import SharedStoreReport


def build_unified_remote_artifact_report(
    *,
    github_reports: list[GitHubArtifactSyncReport] | None = None,
    remote_reader_reports: list[RemoteReaderReport] | None = None,
    shared_store_reports: list[SharedStoreReport] | None = None,
    object_indexes: list[ObjectArtifactIndex] | None = None,
) -> UnifiedRemoteArtifactReport:
    """Build a unified report across all remote artifact sources."""

    github_reports = github_reports or []
    remote_reader_reports = remote_reader_reports or []
    shared_store_reports = shared_store_reports or []
    object_indexes = object_indexes or []

    sources = [
        *[source_from_github(report) for report in github_reports],
        *[source_from_remote_reader(report) for report in remote_reader_reports],
        *[source_from_shared_store(report) for report in shared_store_reports],
        *[source_from_object_store(index) for index in object_indexes],
    ]
    artifacts = [
        *[artifact for report in github_reports for artifact in artifacts_from_github(report)],
        *[
            artifact
            for report in remote_reader_reports
            for artifact in artifacts_from_remote_reader(report)
        ],
        *[
            artifact
            for report in shared_store_reports
            for artifact in artifacts_from_shared_store(report)
        ],
        *[
            artifact
            for index in object_indexes
            for artifact in artifacts_from_object_store(index)
        ],
    ]
    selected = [item for item in artifacts if item.status == RemoteArtifactStatus.SELECTED]
    omitted = [
        item
        for item in artifacts
        if item.status in {RemoteArtifactStatus.OMITTED, RemoteArtifactStatus.METADATA_ONLY}
    ]
    unsafe = [item for item in artifacts if item.status == RemoteArtifactStatus.UNSAFE]
    proposed_imports = [_proposed_import(item) for item in selected]
    evidence_tags = sorted({tag for item in artifacts for tag in item.evidence_tags})
    return UnifiedRemoteArtifactReport(
        sources=sources,
        normalized_artifacts=artifacts,
        duplicate_candidates=_find_duplicate_candidates(artifacts),
        selected_artifacts=selected,
        omitted_artifacts=omitted,
        unsafe_artifacts=unsafe,
        proposed_imports=proposed_imports,
        evidence_tags=evidence_tags,
        requires_human_review=True,
        human_verified=False,
        limitations=[
            "Remote artifact integration normalizes metadata only.",
            "Proposed imports are not written to Evidence Ledger automatically.",
            "Remote artifacts are indexed or retrieved, not human verified.",
            "Unsafe files and large payloads remain omitted or metadata-only.",
        ],
    )


def _find_duplicate_candidates(artifacts: list[ArtifactRef]) -> list[list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for artifact in artifacts:
        groups[duplicate_key(artifact.path, artifact.sha256)].append(artifact.artifact_id)
    return [sorted(values) for values in groups.values() if len(values) > 1]


def _proposed_import(artifact: ArtifactRef) -> dict[str, object]:
    return {
        "artifact_id": artifact.artifact_id,
        "source_id": artifact.source_id,
        "source_kind": artifact.source_kind,
        "path": artifact.path,
        "status": "requires-human-review",
        "sha256": artifact.sha256,
    }
