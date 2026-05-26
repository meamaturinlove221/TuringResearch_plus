from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.export_audit import (
    ExportAuditSeverity,
    audit_export_file,
)


def test_export_audit_detects_unsafe_claim(tmp_path: Path) -> None:
    path = tmp_path / "report.md"
    path.write_text("SparseConv3D success is complete.\n", encoding="utf-8")

    audit = audit_export_file(path)

    assert audit.exists is True
    assert any(finding.check_id == "unsafe-claim" for finding in audit.findings)


def test_export_audit_records_skipped_reason(tmp_path: Path) -> None:
    path = tmp_path / "pdf_export_report.md"
    path.write_text(
        "- status: skipped\n- skipped_reason: backend missing\n",
        encoding="utf-8",
    )

    audit = audit_export_file(path)

    assert audit.skipped is True
    assert audit.skipped_reason == "backend missing"
    assert audit.findings == []


def test_export_audit_flags_missing_output(tmp_path: Path) -> None:
    audit = audit_export_file(tmp_path / "missing.md")

    assert audit.exists is False
    assert audit.findings[0].severity == ExportAuditSeverity.ERROR
