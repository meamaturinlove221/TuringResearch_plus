"""Local bundle ingestor for fixture and exported run packages."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from turing_research_plus.run_ingest.models import RunIngestReport, RunIngestRequest
from turing_research_plus.run_ingest.report_builder import build_run_ingest_report


def ingest_local_bundle(request: RunIngestRequest) -> RunIngestReport:
    """Ingest a local run bundle without executing anything."""

    payload = load_bundle_payload(request.source_path)
    if request.run_id:
        payload["run_id"] = request.run_id
    if request.route_id:
        payload.setdefault("route_id", request.route_id)
    return build_run_ingest_report(
        source_type=request.source_type,
        source_path=request.source_path,
        payload=payload,
    )


def load_bundle_payload(source_path: Path) -> dict[str, Any]:
    """Load bundle metadata from a directory or JSON file."""

    if source_path.is_dir():
        final_status = source_path / "final_status.json"
        if final_status.exists():
            return json.loads(final_status.read_text(encoding="utf-8-sig"))
        return {"run_id": source_path.name, "status": "UNKNOWN", "artifacts": []}
    if source_path.suffix.lower() == ".json":
        return json.loads(source_path.read_text(encoding="utf-8-sig"))
    return {"run_id": source_path.stem, "status": "UNKNOWN", "artifacts": []}
