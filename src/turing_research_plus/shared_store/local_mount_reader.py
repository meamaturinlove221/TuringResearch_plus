"""Read-only scanner for already mounted NAS/SMB shared store paths."""

from __future__ import annotations

import hashlib
from pathlib import Path

from turing_research_plus.remote_readers.safety import (
    omitted_reason_for_remote_file,
    safety_warnings_for_remote_path,
)
from turing_research_plus.shared_store.lock_policy import evaluate_lock_status
from turing_research_plus.shared_store.models import (
    SharedStoreFileRef,
    SharedStoreFileStatus,
    SharedStoreReport,
    SharedStoreScanRequest,
    SharedStoreScanStatus,
)


def scan_local_mount(request: SharedStoreScanRequest) -> SharedStoreReport:
    """Scan an already mounted local path without mutating it."""

    root = request.root_path.resolve()
    if not root.exists() or not root.is_dir():
        return SharedStoreReport(
            mount_label=request.mount_label,
            root_path=request.root_path,
            scan_status=SharedStoreScanStatus.ROOT_MISSING,
            errors=[f"shared store root does not exist or is not a directory: {root}"],
            limitations=["TuringResearch does not mount SMB or handle credentials."],
        )

    lock_status = evaluate_lock_status(
        root,
        require_lock_file=request.require_lock_file,
        lock_file_name=request.lock_file_name,
    )
    selected_files: list[SharedStoreFileRef] = []
    omitted_files: list[SharedStoreFileRef] = []
    large_files: list[SharedStoreFileRef] = []
    unsafe_files: list[SharedStoreFileRef] = []
    all_warnings: list[str] = []
    manifest: dict[str, str] = {}

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if request.selected_patterns and not any(
            pattern in relative for pattern in request.selected_patterns
        ):
            continue
        size = path.stat().st_size
        warnings = safety_warnings_for_remote_path(
            relative,
            root_path=None,
            size=size,
            max_size=request.max_file_size_bytes,
            is_symlink=path.is_symlink(),
        )
        all_warnings.extend(warnings)
        sha256 = _sha256_file(path) if request.compute_sha256 and not warnings else None
        status = _status_for_warnings(warnings)
        file_ref = SharedStoreFileRef(
            relative_path=relative,
            absolute_path=path,
            size=size,
            sha256=sha256,
            content_type=_content_type_for_path(path),
            status=status,
            omitted_reason=omitted_reason_for_remote_file(warnings) if warnings else None,
            safety_warnings=warnings,
        )
        if sha256:
            manifest[relative] = sha256
        if status == SharedStoreFileStatus.SELECTED:
            selected_files.append(file_ref)
        elif status == SharedStoreFileStatus.LARGE_METADATA_ONLY:
            large_files.append(file_ref)
            omitted_files.append(file_ref)
        elif status == SharedStoreFileStatus.UNSAFE:
            unsafe_files.append(file_ref)
            omitted_files.append(file_ref)
        else:
            omitted_files.append(file_ref)

    proposed_imports = [
        {
            "relative_path": item.relative_path,
            "status": "requires-human-review",
            "mount_label": request.mount_label,
            "sha256": item.sha256,
        }
        for item in selected_files
    ]
    return SharedStoreReport(
        mount_label=request.mount_label,
        root_path=root,
        scan_status=SharedStoreScanStatus.INDEXED,
        lock_status=lock_status,
        selected_files=selected_files,
        omitted_files=omitted_files,
        large_files=large_files,
        unsafe_files=unsafe_files,
        proposed_imports=proposed_imports,
        manifest=manifest,
        safety_warnings=sorted(set(all_warnings)),
        requires_human_review=True,
        human_verified=False,
        limitations=[
            "Shared store scanner reads an already mounted local path only.",
            "TuringResearch does not mount SMB or handle credentials.",
            "Selected artifacts are indexed, not human verified.",
            "Evidence Ledger is not overwritten automatically.",
        ],
    )


def _status_for_warnings(warnings: list[str]) -> SharedStoreFileStatus:
    if not warnings:
        return SharedStoreFileStatus.SELECTED
    if any(
        warning
        in {
            "forbidden-env-file",
            "forbidden-private-or-cache-path",
            "forbidden-secret-or-body-model-pattern",
            "path-traversal",
            "symlink-requires-review",
        }
        for warning in warnings
    ):
        return SharedStoreFileStatus.UNSAFE
    if "file-too-large" in warnings or "summary-only-required" in warnings:
        return SharedStoreFileStatus.LARGE_METADATA_ONLY
    return SharedStoreFileStatus.OMITTED


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _content_type_for_path(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".md": "text/markdown",
        ".txt": "text/plain",
        ".json": "application/json",
        ".yaml": "application/yaml",
        ".yml": "application/yaml",
        ".csv": "text/csv",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
    }.get(suffix, "application/octet-stream")
