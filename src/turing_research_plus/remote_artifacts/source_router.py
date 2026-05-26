"""Normalize source-specific reports into unified artifact refs."""

from __future__ import annotations

from turing_research_plus.github_sync.models import GitHubArtifactSyncReport
from turing_research_plus.object_store.models import ObjectArtifactIndex, ObjectArtifactStatus
from turing_research_plus.remote_artifacts.models import (
    ArtifactRef,
    RemoteArtifactSource,
    RemoteArtifactSourceKind,
    RemoteArtifactStatus,
)
from turing_research_plus.remote_artifacts.safety import (
    stable_artifact_id,
    unified_status_from_warnings,
)
from turing_research_plus.remote_readers.models import RemoteReaderReport
from turing_research_plus.shared_store.models import SharedStoreFileStatus, SharedStoreReport


def source_from_github(report: GitHubArtifactSyncReport) -> RemoteArtifactSource:
    """Build a source descriptor from a GitHub report."""

    return RemoteArtifactSource(
        source_id=f"github:{report.source_repo}:{report.source_ref}",
        kind=RemoteArtifactSourceKind.GITHUB,
        label=report.source_repo,
        locator=report.source_ref,
        retrieval_status=str(report.retrieval_status),
        live_result=report.live_result,
    )


def artifacts_from_github(report: GitHubArtifactSyncReport) -> list[ArtifactRef]:
    """Normalize GitHub selected and omitted artifacts."""

    source = source_from_github(report)
    artifacts: list[ArtifactRef] = []
    for selected_file in report.selected_files:
        artifacts.append(
            ArtifactRef(
                artifact_id=stable_artifact_id(source.source_id, selected_file.path),
                source_id=source.source_id,
                source_kind=source.kind,
                path=selected_file.path,
                size=selected_file.size,
                sha256=selected_file.sha256,
                status=RemoteArtifactStatus.SELECTED,
                safety_warnings=selected_file.warnings,
            )
        )
    for omitted_file in report.omitted_files:
        artifacts.append(
            ArtifactRef(
                artifact_id=stable_artifact_id(source.source_id, omitted_file.path),
                source_id=source.source_id,
                source_kind=source.kind,
                path=omitted_file.path,
                size=omitted_file.size,
                status=unified_status_from_warnings(omitted_file.safety_warnings),
                omitted_reason=omitted_file.reason,
                safety_warnings=omitted_file.safety_warnings,
            )
        )
    return artifacts


def source_from_remote_reader(report: RemoteReaderReport) -> RemoteArtifactSource:
    """Build a source descriptor from an SSH/SFTP remote reader report."""

    return RemoteArtifactSource(
        source_id=f"ssh_sftp:{report.host_label}:{report.root_path}",
        kind=RemoteArtifactSourceKind.SSH_SFTP,
        label=report.host_label,
        locator=report.root_path,
        retrieval_status=str(report.retrieval_status),
        live_result=report.live_result,
    )


def artifacts_from_remote_reader(report: RemoteReaderReport) -> list[ArtifactRef]:
    """Normalize SSH/SFTP selected and omitted artifacts."""

    source = source_from_remote_reader(report)
    artifacts: list[ArtifactRef] = []
    for selected_file in report.selected_files:
        artifacts.append(
            ArtifactRef(
                artifact_id=stable_artifact_id(source.source_id, selected_file.path),
                source_id=source.source_id,
                source_kind=source.kind,
                path=selected_file.path,
                size=selected_file.size,
                sha256=selected_file.sha256,
                status=RemoteArtifactStatus.SELECTED,
                safety_warnings=selected_file.warnings,
            )
        )
    for omitted_file in report.omitted_files:
        artifacts.append(
            ArtifactRef(
                artifact_id=stable_artifact_id(source.source_id, omitted_file.path),
                source_id=source.source_id,
                source_kind=source.kind,
                path=omitted_file.path,
                size=omitted_file.size,
                status=unified_status_from_warnings(omitted_file.safety_warnings),
                omitted_reason=omitted_file.reason,
                safety_warnings=omitted_file.safety_warnings,
            )
        )
    return artifacts


def source_from_shared_store(report: SharedStoreReport) -> RemoteArtifactSource:
    """Build a source descriptor from a shared store report."""

    return RemoteArtifactSource(
        source_id=f"nas_smb:{report.mount_label}:{report.root_path}",
        kind=RemoteArtifactSourceKind.NAS_SMB,
        label=report.mount_label,
        locator=str(report.root_path),
        retrieval_status=str(report.scan_status),
        live_result=False,
    )


def artifacts_from_shared_store(report: SharedStoreReport) -> list[ArtifactRef]:
    """Normalize NAS/SMB shared store artifacts."""

    source = source_from_shared_store(report)
    artifacts: list[ArtifactRef] = []
    for item in [*report.selected_files, *report.omitted_files]:
        status = _status_from_shared_store(item.status)
        artifacts.append(
            ArtifactRef(
                artifact_id=stable_artifact_id(source.source_id, item.relative_path),
                source_id=source.source_id,
                source_kind=source.kind,
                path=item.relative_path,
                size=item.size,
                sha256=item.sha256,
                content_type=item.content_type,
                status=status,
                omitted_reason=item.omitted_reason,
                safety_warnings=item.safety_warnings,
            )
        )
    return artifacts


def source_from_object_store(index: ObjectArtifactIndex) -> RemoteArtifactSource:
    """Build a source descriptor from an object artifact index."""

    return RemoteArtifactSource(
        source_id=f"cloud_object:{index.provider}:{index.bucket_or_container}:{index.prefix}",
        kind=RemoteArtifactSourceKind.CLOUD_OBJECT,
        label=f"{index.provider}/{index.bucket_or_container}",
        locator=index.prefix,
        retrieval_status=str(index.status),
        live_result=False,
    )


def artifacts_from_object_store(index: ObjectArtifactIndex) -> list[ArtifactRef]:
    """Normalize cloud object artifact refs."""

    source = source_from_object_store(index)
    return [
        ArtifactRef(
            artifact_id=stable_artifact_id(source.source_id, item.key),
            source_id=source.source_id,
            source_kind=source.kind,
            path=item.key,
            size=item.size,
            sha256=item.hash,
            content_type=item.content_type,
            status=_status_from_object_store(item.status),
            omitted_reason=item.omitted_reason,
            safety_warnings=item.safety_warnings,
            evidence_tags=item.evidence_tags,
        )
        for item in index.objects
    ]


def _status_from_shared_store(status: SharedStoreFileStatus) -> RemoteArtifactStatus:
    if status == SharedStoreFileStatus.SELECTED:
        return RemoteArtifactStatus.SELECTED
    if status == SharedStoreFileStatus.LARGE_METADATA_ONLY:
        return RemoteArtifactStatus.METADATA_ONLY
    if status == SharedStoreFileStatus.UNSAFE:
        return RemoteArtifactStatus.UNSAFE
    return RemoteArtifactStatus.OMITTED


def _status_from_object_store(status: ObjectArtifactStatus) -> RemoteArtifactStatus:
    if status == ObjectArtifactStatus.SELECTED:
        return RemoteArtifactStatus.SELECTED
    if status == ObjectArtifactStatus.LARGE_METADATA_ONLY:
        return RemoteArtifactStatus.METADATA_ONLY
    if status == ObjectArtifactStatus.UNSAFE:
        return RemoteArtifactStatus.UNSAFE
    if status == ObjectArtifactStatus.ERROR:
        return RemoteArtifactStatus.ERROR
    return RemoteArtifactStatus.OMITTED
