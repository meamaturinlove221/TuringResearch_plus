"""Fake/local transfer implementation for context pack handoff."""

from __future__ import annotations

import shutil
from pathlib import Path

from turing_research_plus.pod_lifecycle.transfer_policy import transfer_warnings_for_path
from turing_research_plus.session_runtime.archive_safety import normalize_pack_entry
from turing_research_plus.session_runtime.archive_writer import sha256_file
from turing_research_plus.session_runtime.transfer_report import (
    TransferFileRecord,
    TransferMode,
    TransferOmittedFile,
    TransferReport,
    TransferStatus,
    collect_source_files,
)


def run_fake_transfer(
    *,
    transfer_id: str,
    package_id: str,
    source_dir: Path,
    target_dir: Path,
) -> TransferReport:
    """Copy safe direct files from source_dir to target_dir without networking."""

    selected: list[TransferFileRecord] = []
    omitted: list[TransferOmittedFile] = []
    errors: list[str] = []

    if not source_dir.exists() or not source_dir.is_dir():
        return TransferReport(
            transfer_id=transfer_id,
            package_id=package_id,
            mode=TransferMode.FAKE,
            status=TransferStatus.BLOCKED,
            source_dir=source_dir.as_posix(),
            target=target_dir.as_posix(),
            errors=["source directory is missing"],
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    for source_path in collect_source_files(source_dir):
        relative = normalize_pack_entry(source_path.relative_to(source_dir))
        warnings = transfer_warnings_for_path(relative, file_size=source_path.stat().st_size)
        if warnings:
            omitted.append(
                TransferOmittedFile(
                    path=relative,
                    reason="omitted by transfer safety policy",
                    warnings=warnings,
                )
            )
            continue
        target_path = target_dir / relative
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
            selected.append(
                TransferFileRecord(
                    path=relative,
                    sha256=sha256_file(target_path),
                    size_bytes=target_path.stat().st_size,
                    source_path=source_path.as_posix(),
                    target_path=target_path.as_posix(),
                    transferred=True,
                )
            )
        except OSError as exc:
            errors.append(f"failed to copy {relative}: {exc}")

    status = TransferStatus.BLOCKED if errors else TransferStatus.TRANSFERRED
    return TransferReport(
        transfer_id=transfer_id,
        package_id=package_id,
        mode=TransferMode.FAKE,
        status=status,
        source_dir=source_dir.as_posix(),
        target=target_dir.as_posix(),
        selected_files=selected,
        omitted_files=omitted,
        errors=errors,
        live_enabled=False,
    )
