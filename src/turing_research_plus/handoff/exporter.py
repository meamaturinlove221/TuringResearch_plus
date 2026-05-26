"""Controlled handoff bundle export."""

from __future__ import annotations

import shutil
from pathlib import Path

from turing_research_plus.handoff.manifest import (
    manifest_to_yaml,
    sha256_file,
    sha256_manifest,
)
from turing_research_plus.handoff.models import (
    HandoffBundleManifest,
    HandoffExportRequest,
    HandoffFileRecord,
)
from turing_research_plus.handoff.safety import omitted_reason, safety_warnings_for_path


def export_handoff_bundle(request: HandoffExportRequest) -> HandoffBundleManifest:
    """Export a local handoff bundle with safety omissions."""

    bundle_dir = request.output_dir / request.bundle_id
    bundle_dir.mkdir(parents=True, exist_ok=True)
    included: list[HandoffFileRecord] = []
    omitted: list[HandoffFileRecord] = []
    warnings: list[str] = []

    for source in request.file_paths:
        source_path = source if source.is_absolute() else request.source_root / source
        relative_path = _relative_to_root(source_path, request.source_root)
        if not source_path.exists() or not source_path.is_file():
            omitted.append(
                HandoffFileRecord(
                    relative_path=relative_path,
                    included=False,
                    omitted_reason="source file missing",
                    safety_warnings=["missing"],
                )
            )
            continue
        file_size = source_path.stat().st_size
        file_warnings = safety_warnings_for_path(
            source_path,
            file_size=file_size,
            max_size=request.max_file_size_bytes,
        )
        if file_warnings:
            omitted.append(
                HandoffFileRecord(
                    relative_path=relative_path,
                    included=False,
                    file_size=file_size,
                    sha256=sha256_file(source_path),
                    omitted_reason=omitted_reason(source_path, file_warnings),
                    safety_warnings=file_warnings,
                )
            )
            warnings.extend(file_warnings)
            continue
        destination = bundle_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        included.append(
            HandoffFileRecord(
                relative_path=relative_path,
                included=True,
                file_size=file_size,
                sha256=sha256_file(destination),
            )
        )

    manifest = HandoffBundleManifest(
        bundle_id=request.bundle_id,
        source_machine_label=request.source_machine_label,
        bundle_type=request.bundle_type,
        included_files=included,
        omitted_files=omitted,
        evidence_tags=request.evidence_tags,
        status_labels=request.status_labels,
        safety_warnings=sorted(set(warnings)),
        manual_review_required=True,
    )
    manifest.sha256 = sha256_manifest(manifest)
    (bundle_dir / "handoff_manifest.yaml").write_text(manifest_to_yaml(manifest), encoding="utf-8")
    (bundle_dir / "HANDOFF_README.md").write_text(_readme(manifest), encoding="utf-8")
    return manifest


def collect_handoff_files(source_root: Path) -> list[Path]:
    """Collect candidate handoff files under source_root using the allow-list policy."""

    candidates: list[Path] = []
    for path in sorted(source_root.rglob("*")):
        if not path.is_file():
            continue
        candidates.append(path.relative_to(source_root))
    return candidates


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def _readme(manifest: HandoffBundleManifest) -> str:
    lines = [
        f"# Handoff Bundle: {manifest.bundle_id}",
        "",
        f"Project: {manifest.project_name}",
        f"Bundle type: `{manifest.bundle_type}`",
        "",
        "This bundle is a controlled TuringResearch Plus handoff artifact. It does not",
        "include raw datasets, secrets, cache folders, or SMPL-X body model files.",
        "",
        "Import must validate `handoff_manifest.yaml` and requires manual review.",
    ]
    return "\n".join(lines) + "\n"
