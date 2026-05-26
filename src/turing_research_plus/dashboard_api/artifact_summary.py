"""Artifact summary builder for dashboard data API."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.models import (
    DashboardArtifactRecord,
    DashboardArtifactSummary,
)


def build_artifact_summary(path: Path) -> DashboardArtifactSummary:
    """Build an artifact summary from the demo artifact Markdown table."""

    parsed_records = [
        _parse_artifact_row(line) for line in path.read_text(encoding="utf-8").splitlines()
    ]
    records: list[DashboardArtifactRecord] = [
        record for record in parsed_records if record is not None
    ]
    return DashboardArtifactSummary(
        records=records,
        selected_count=sum(1 for record in records if record.safety == "selected"),
        omitted_count=sum(1 for record in records if record.safety == "omitted"),
        missing_count=sum(1 for record in records if record.status == "missing"),
    )


def _parse_artifact_row(line: str) -> DashboardArtifactRecord | None:
    stripped = line.strip()
    if not stripped.startswith("|") or "---" in stripped or "Artifact" in stripped:
        return None
    parts = [part.strip().strip("`") for part in stripped.strip("|").split("|")]
    if len(parts) != 5:
        return None
    artifact, status, size, safety, notes = parts
    return DashboardArtifactRecord(
        artifact=artifact,
        status=status,
        size=size,
        safety=safety,
        notes=notes,
    )
