"""Local tool wrappers for read-only remote artifact reading."""

from __future__ import annotations

from turing_research_plus.remote_readers.fake_reader import FakeRemoteArtifactReader
from turing_research_plus.remote_readers.models import (
    RemoteArtifactRecord,
    RemoteOmittedFile,
    RemoteReaderReport,
    RemoteReaderRequest,
    RemoteReaderSourceType,
    RemoteReaderStatus,
    RemoteSelectedFile,
)
from turing_research_plus.remote_readers.safety import (
    omitted_reason_for_remote_file,
    safety_warnings_for_remote_path,
)
from turing_research_plus.remote_readers.sftp_reader import (
    SFTPConnectionSpec,
    SFTPRemoteReader,
)


def read_remote_artifacts(
    request: RemoteReaderRequest,
    *,
    fake_reader: FakeRemoteArtifactReader | None = None,
    sftp_reader: SFTPRemoteReader | None = None,
) -> RemoteReaderReport:
    """Build a read-only remote reader report."""

    artifacts, status, errors, warnings, live_result = _load_artifacts(
        request,
        fake_reader=fake_reader,
        sftp_reader=sftp_reader,
    )
    selected_candidates = _filter_selected(artifacts, request.selected_patterns)
    selected_files: list[RemoteSelectedFile] = []
    omitted_files: list[RemoteOmittedFile] = []
    all_warnings = list(warnings)

    for artifact in selected_candidates:
        safety_warnings = safety_warnings_for_remote_path(
            artifact.path,
            root_path=request.root_path,
            size=artifact.size,
            max_size=request.max_file_size_bytes,
            is_symlink=artifact.is_symlink,
        )
        if safety_warnings:
            omitted_files.append(
                RemoteOmittedFile(
                    path=artifact.path,
                    size=artifact.size,
                    reason=omitted_reason_for_remote_file(safety_warnings),
                    safety_warnings=safety_warnings,
                )
            )
            all_warnings.extend(safety_warnings)
            continue
        selected_files.append(
            RemoteSelectedFile(
                path=artifact.path,
                size=artifact.size,
                sha256=artifact.sha256,
                retrieval_status=RemoteReaderStatus.RETRIEVED
                if request.allow_download and live_result
                else RemoteReaderStatus.SELECTED,
                source_type=artifact.source_type,
                verified=False,
                warnings=["remote artifact is indexed or retrieved, not human verified"],
            )
        )

    proposed_imports = [
        {
            "path": item.path,
            "status": "requires-human-review",
            "host_label": request.host_label,
            "root_path": request.root_path,
        }
        for item in selected_files
    ]
    scanned_paths = sorted({artifact.path for artifact in artifacts})
    return RemoteReaderReport(
        host_label=request.host_label,
        root_path=request.root_path,
        retrieval_status=status,
        scanned_paths=scanned_paths,
        artifact_list=artifacts,
        selected_files=selected_files,
        omitted_files=omitted_files,
        errors=errors,
        safety_warnings=sorted(set(all_warnings)),
        proposed_imports=proposed_imports,
        requires_human_review=True,
        live_result=live_result,
        human_verified=False,
        limitations=[
            "Remote reader is read-only and does not execute remote commands.",
            "Remote artifacts are indexed or retrieved, not human verified.",
            "Evidence Ledger is not overwritten automatically.",
        ],
    )


def _load_artifacts(
    request: RemoteReaderRequest,
    *,
    fake_reader: FakeRemoteArtifactReader | None,
    sftp_reader: SFTPRemoteReader | None,
) -> tuple[list[RemoteArtifactRecord], RemoteReaderStatus, list[str], list[str], bool]:
    if request.fixture_index_path is not None:
        reader = FakeRemoteArtifactReader(request.fixture_index_path)
        return (
            reader.list_artifacts(request.root_path),
            RemoteReaderStatus.INDEXED,
            [],
            ["local fixture index; no network access performed"],
            False,
        )
    if request.dry_run:
        reader = fake_reader or FakeRemoteArtifactReader()
        return (
            reader.list_artifacts(request.root_path),
            RemoteReaderStatus.INDEXED,
            [],
            ["fake SFTP reader; no network access"],
            False,
        )
    if not request.live_enabled:
        return [], RemoteReaderStatus.LIVE_DISABLED, [], ["SFTP live reader is disabled"], False

    live_reader = sftp_reader or SFTPRemoteReader(
        SFTPConnectionSpec(
            host_label=request.host_label,
            root_path=request.root_path,
            credential_env=request.credential_env,
        )
    )
    if not live_reader.has_credential():
        return (
            [],
            RemoteReaderStatus.MISSING_CREDENTIAL,
            [live_reader.missing_credential_error()],
            [],
            False,
        )
    try:
        artifacts = live_reader.list_artifacts()
    except Exception as exc:  # pragma: no cover - live path guarded by optional tests
        return [], RemoteReaderStatus.ERROR, [f"SFTP live reader failed: {exc}"], [], True
    return (
        artifacts,
        RemoteReaderStatus.RETRIEVED,
        [],
        ["live remote result is retrieved, not verified"],
        True,
    )


def _filter_selected(
    artifacts: list[RemoteArtifactRecord],
    selected_patterns: list[str],
) -> list[RemoteArtifactRecord]:
    if not selected_patterns:
        return artifacts
    return [
        artifact
        for artifact in artifacts
        if any(pattern in artifact.path for pattern in selected_patterns)
    ]


def artifact_sftp_read_optional(request: RemoteReaderRequest) -> RemoteReaderReport:
    """Tool-style wrapper for read-only remote artifact inspection."""

    return read_remote_artifacts(request)


__all__ = [
    "RemoteReaderSourceType",
    "RemoteReaderStatus",
    "artifact_sftp_read_optional",
    "read_remote_artifacts",
]
