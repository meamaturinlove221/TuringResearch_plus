"""Minimal read-only artifact auditor."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from tuling_research_plus.artifact_audit.manifest import infer_file_type, load_manifest_like_index
from tuling_research_plus.artifact_audit.models import (
    ArtifactAuditInput,
    ArtifactAuditReport,
    ArtifactFileType,
    ArtifactRecord,
    ArtifactSafetyFlag,
)
from tuling_research_plus.artifact_audit.npz_summary import summarize_npz


def audit_artifacts(request: ArtifactAuditInput) -> ArtifactAuditReport:
    """Audit local manifest-like artifact input without reading private VGGT paths."""

    manifest = load_manifest_like_index(request.source_path)
    records: list[ArtifactRecord] = []
    safety_flags: list[ArtifactSafetyFlag] = []
    warnings = list(manifest.warnings)

    for record in manifest.records:
        audited = _audit_record(record, request)
        records.append(audited)
        safety_flags.extend(audited.safety_flags)

    if not manifest.records:
        warnings.append("Artifact audit found no artifact records.")

    return ArtifactAuditReport(
        report_id=f"{request.source_path.stem}-artifact-audit",
        source_path=str(request.source_path),
        records=records,
        included_count=sum(1 for record in records if record.included),
        omitted_count=sum(1 for record in records if not record.included),
        warnings=list(dict.fromkeys(warnings)),
        safety_flags=list(dict.fromkeys(safety_flags)),
    )


def artifact_audit(request: ArtifactAuditInput) -> dict[str, Any]:
    """Capsule-local thin wrapper for the proposed artifact.audit tool."""

    return audit_artifacts(request).model_dump(mode="json")


def _audit_record(record: ArtifactRecord, request: ArtifactAuditInput) -> ArtifactRecord:
    candidate = Path(record.path)
    resolved = _resolve_candidate(candidate, request.base_dir)
    flags = list(record.safety_flags)

    if _is_external_or_private_reference(candidate):
        flags.extend(
            [
                ArtifactSafetyFlag.EXTERNAL_PATH_REFERENCE,
                ArtifactSafetyFlag.PRIVATE_PATH_NOT_READ,
            ]
        )
        return record.model_copy(
            update={
                "included": False,
                "omitted_reason": record.omitted_reason
                or "external or private path reference was not read",
                "safety_flags": list(dict.fromkeys(flags)),
            }
        )

    file_size = record.file_size
    sha256 = record.sha256
    npz_summary = record.npz_summary
    if resolved is not None and resolved.exists() and resolved.is_file():
        file_size = resolved.stat().st_size
        if request.compute_sha256:
            sha256 = _sha256_file(resolved)
        elif record.sha256 is None:
            flags.append(ArtifactSafetyFlag.HASH_SKIPPED)
        if request.summarize_npz and infer_file_type(resolved) == ArtifactFileType.NPZ:
            npz_summary = summarize_npz(resolved)
        elif infer_file_type(resolved) == ArtifactFileType.NPZ:
            flags.append(ArtifactSafetyFlag.NPZ_SUMMARY_PLACEHOLDER)

    return record.model_copy(
        update={
            "file_type": record.file_type
            if record.file_type != ArtifactFileType.UNKNOWN
            else infer_file_type(record.path),
            "file_size": file_size,
            "sha256": sha256,
            "safety_flags": list(dict.fromkeys(flags or [ArtifactSafetyFlag.LOCAL_ONLY])),
            "npz_summary": npz_summary,
        }
    )


def _resolve_candidate(path: Path, base_dir: Path | None) -> Path | None:
    if path.is_absolute():
        return path
    if base_dir is None:
        return None
    return base_dir / path


def _is_external_or_private_reference(path: Path) -> bool:
    raw = str(path).replace("\\", "/").lower()
    return raw.startswith("d:/vggt") or "/private_data/" in raw or "/secrets/" in raw


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

