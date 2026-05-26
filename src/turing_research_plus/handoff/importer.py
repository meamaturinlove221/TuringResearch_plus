"""Controlled handoff bundle import validation."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.manifest import manifest_from_yaml, sha256_file
from turing_research_plus.handoff.models import (
    HandoffBundleImportReport,
    HandoffImportRequest,
)
from turing_research_plus.handoff.safety import safety_warnings_for_path


def import_handoff_bundle(request: HandoffImportRequest) -> HandoffBundleImportReport:
    """Validate a handoff bundle without overwriting local project state."""

    manifest_path = request.bundle_dir / "handoff_manifest.yaml"
    if not manifest_path.exists():
        return HandoffBundleImportReport(
            bundle_id=request.bundle_dir.name,
            valid_manifest=False,
            missing_files=["handoff_manifest.yaml"],
            proposed_updates=[{"status": "requires-human-review", "reason": "manifest missing"}],
        )

    try:
        manifest = manifest_from_yaml(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation report must not crash callers.
        return HandoffBundleImportReport(
            bundle_id=request.bundle_dir.name,
            valid_manifest=False,
            unsafe_files=["handoff_manifest.yaml"],
            proposed_updates=[
                {
                    "status": "requires-human-review",
                    "reason": f"manifest parse failed: {exc}",
                }
            ],
        )

    missing: list[str] = []
    unsafe: list[str] = []
    verified: list[str] = []
    mismatches: list[str] = []
    warnings = list(manifest.safety_warnings)

    for record in manifest.included_files:
        path = request.bundle_dir / Path(record.relative_path)
        if not path.exists() or not path.is_file():
            missing.append(record.relative_path)
            continue

        file_warnings = safety_warnings_for_path(path, file_size=path.stat().st_size)
        if file_warnings:
            unsafe.append(record.relative_path)
            warnings.extend(file_warnings)

        if request.verify_sha256 and record.sha256:
            actual = sha256_file(path)
            if actual != record.sha256:
                mismatches.append(record.relative_path)
            else:
                verified.append(record.relative_path)
        else:
            verified.append(record.relative_path)

    for record in manifest.omitted_files:
        warnings.extend(record.safety_warnings)

    proposed_updates = [
        {
            "bundle_id": manifest.bundle_id,
            "status": "requires-human-review",
            "reason": "handoff import validation only; evidence ledger is not overwritten",
            "evidence_tags": manifest.evidence_tags,
            "status_labels": [str(item) for item in manifest.status_labels],
        }
    ]

    return HandoffBundleImportReport(
        bundle_id=manifest.bundle_id,
        valid_manifest=True,
        verified_files=verified,
        missing_files=missing,
        unsafe_files=unsafe,
        sha256_mismatches=mismatches,
        proposed_updates=proposed_updates,
        safety_warnings=sorted(set(warnings)),
        manual_review_required=True,
    )
