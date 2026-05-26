import pytest

from turing_research_plus.artifact_audit.models import (
    ArtifactAuditReport,
    ArtifactFileType,
    ArtifactRecord,
)


def test_omitted_artifact_requires_reason() -> None:
    with pytest.raises(ValueError, match="omitted_reason"):
        ArtifactRecord(path="missing.npz", file_type=ArtifactFileType.NPZ, included=False)


def test_audit_report_counts_must_match_records() -> None:
    with pytest.raises(ValueError, match="counts"):
        ArtifactAuditReport(
            report_id="report",
            source_path="manifest.json",
            records=[ArtifactRecord(path="a.json", file_type=ArtifactFileType.JSON)],
            included_count=0,
            omitted_count=0,
        )


def test_audit_report_markdown_contains_records() -> None:
    report = ArtifactAuditReport(
        report_id="report",
        source_path="manifest.json",
        records=[ArtifactRecord(path="a.json", file_type=ArtifactFileType.JSON)],
        included_count=1,
        omitted_count=0,
    )

    assert "a.json" in report.to_markdown()

