from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.quality_gate import (
    ExportQualityGateRequest,
    ExportQualityStatus,
    run_export_quality_gate,
)

ROOT = Path(__file__).resolve().parents[2]
ADVISOR_EXPORT = ROOT / "examples" / "vggt-human-prior-survey" / "advisor_export"
DASHBOARD = (
    ROOT
    / "examples"
    / "vggt-human-prior-survey"
    / "dashboard_html"
    / "refined_dashboard.html"
)


def test_vggt_export_quality_gate_fixture() -> None:
    report = run_export_quality_gate(
        ExportQualityGateRequest(
            advisor_export_dir=ADVISOR_EXPORT,
            dashboard_paths=[DASHBOARD],
        )
    )

    assert report.status == ExportQualityStatus.PASS_WITH_WARNINGS
    assert report.requires_human_review is True
    assert len(report.skipped_outputs) == 2
    assert not any(finding.severity == "error" for finding in report.findings)


def test_committed_vggt_export_quality_report_exists() -> None:
    report = (ADVISOR_EXPORT / "export_quality_report.md").read_text(encoding="utf-8")

    assert "status: pass-with-warnings" in report
    assert "pdf_export_report.md" in report
    assert "pptx_export_report.md" in report
    assert "requires_human_review: true" in report
