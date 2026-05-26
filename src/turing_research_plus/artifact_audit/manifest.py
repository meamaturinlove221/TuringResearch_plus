"""Manifest and local scan index parsing for artifact audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tuling_research_plus.artifact_audit.models import (
    ArtifactBundleManifest,
    ArtifactFileType,
    ArtifactRecord,
    ArtifactSafetyFlag,
)


def load_manifest_like_index(path: Path) -> ArtifactBundleManifest:
    """Load a JSON manifest or Markdown local scan artifact index."""

    if not path.exists():
        return ArtifactBundleManifest(
            manifest_id=f"{path.stem}-missing",
            source=str(path),
            warnings=[f"Manifest-like index missing: {path}"],
        )
    if path.suffix.lower() == ".json":
        return _load_json_manifest(path)
    return _load_markdown_index(path)


def infer_file_type(path: str | Path) -> ArtifactFileType:
    """Infer a stable artifact file type from suffix."""

    suffix = Path(str(path)).suffix.lower().lstrip(".")
    return {
        "zip": ArtifactFileType.ZIP,
        "json": ArtifactFileType.JSON,
        "csv": ArtifactFileType.CSV,
        "png": ArtifactFileType.PNG,
        "jpg": ArtifactFileType.JPG,
        "jpeg": ArtifactFileType.JPG,
        "npz": ArtifactFileType.NPZ,
        "md": ArtifactFileType.MD,
    }.get(suffix, ArtifactFileType.UNKNOWN)


def _load_json_manifest(path: Path) -> ArtifactBundleManifest:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_records = payload.get("artifacts", payload.get("records", []))
    records = [_record_from_json(item) for item in raw_records if isinstance(item, dict)]
    warnings = payload.get("warnings", [])
    return ArtifactBundleManifest(
        manifest_id=payload.get("manifest_id", path.stem),
        source=str(path),
        records=records,
        warnings=warnings,
    )


def _record_from_json(payload: dict[str, Any]) -> ArtifactRecord:
    raw_flags = payload.get("safety_flags", [])
    return ArtifactRecord(
        path=str(payload["path"]),
        file_type=ArtifactFileType(payload.get("file_type", infer_file_type(payload["path"]))),
        file_size=payload.get("file_size"),
        sha256=payload.get("sha256"),
        included=payload.get("included", True),
        omitted_reason=payload.get("omitted_reason"),
        safety_flags=[ArtifactSafetyFlag(flag) for flag in raw_flags],
        metadata=payload.get("metadata", {}),
    )


def _load_markdown_index(path: Path) -> ArtifactBundleManifest:
    text = path.read_text(encoding="utf-8")
    if "No artifacts were scanned" in text:
        return ArtifactBundleManifest(
            manifest_id=path.stem,
            source=str(path),
            records=[],
            warnings=["No artifacts were scanned in this dry run."],
        )

    records: list[ArtifactRecord] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped or "Path" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if not cells or not cells[0]:
            continue
        record_path = cells[0].strip("`")
        included = len(cells) < 4 or cells[3].lower() not in {"false", "no", "omitted"}
        omitted_reason = None if included else "marked omitted in local scan index"
        records.append(
            ArtifactRecord(
                path=record_path,
                file_type=infer_file_type(record_path),
                included=included,
                omitted_reason=omitted_reason,
                safety_flags=[ArtifactSafetyFlag.LOCAL_ONLY],
            )
        )
    return ArtifactBundleManifest(
        manifest_id=path.stem,
        source=str(path),
        records=records,
    )

