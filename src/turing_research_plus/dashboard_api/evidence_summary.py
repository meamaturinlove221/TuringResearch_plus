"""Evidence summary builder for dashboard data API."""

from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.dashboard_api.models import (
    DashboardEvidenceEntry,
    DashboardEvidenceSummary,
)


def build_evidence_summary(path: Path) -> DashboardEvidenceSummary:
    """Build an evidence summary from a public demo ledger JSON file."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    entries = [
        DashboardEvidenceEntry(
            evidence_id=str(item["evidence_id"]),
            status=str(item["status"]),
            claim=str(item["claim"]),
            source_ref=str(item["source_ref"]),
            notes=str(item.get("notes", "")),
        )
        for item in payload.get("entries", [])
    ]
    counts: dict[str, int] = {}
    for entry in entries:
        counts[entry.status] = counts.get(entry.status, 0) + 1
    return DashboardEvidenceSummary(
        ledger_id=str(payload["ledger_id"]),
        status=str(payload["status"]),
        entries=entries,
        status_counts=counts,
        limitations=[str(item) for item in payload.get("limitations", [])],
    )
