from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.quality_gate import (
    ExportQualityGateRequest,
    ExportQualityStatus,
    render_export_quality_report,
    run_export_quality_gate,
)


def _write_minimal_export_dir(root: Path) -> None:
    (root / "pdf_export").mkdir(parents=True)
    (root / "pptx_export").mkdir(parents=True)
    (root / "advisor_report_source.md").write_text("review source\n", encoding="utf-8")
    (root / "evidence_refs.md").write_text(
        "Evidence refs require human review.\n",
        encoding="utf-8",
    )
    (root / "limitations.md").write_text(
        "Does not run experiments. Requires human review.\n",
        encoding="utf-8",
    )
    (root / "next_actions.md").write_text("Collect missing artifacts.\n", encoding="utf-8")
    (root / "pdf_export" / "pdf_export_report.md").write_text(
        "- status: skipped\n- skipped_reason: backend missing\n",
        encoding="utf-8",
    )
    (root / "pdf_export" / "advisor_pdf_review_source.md").write_text(
        "PDF review source with limitations.\n",
        encoding="utf-8",
    )
    (root / "pptx_export" / "pptx_export_report.md").write_text(
        "- status: skipped\n- skipped_reason: backend missing\n",
        encoding="utf-8",
    )
    (root / "pptx_export" / "advisor_pptx_review_source.md").write_text(
        "PPTX review source with limitations.\n",
        encoding="utf-8",
    )


def test_export_quality_gate_passes_with_skipped_outputs(tmp_path: Path) -> None:
    _write_minimal_export_dir(tmp_path)

    report = run_export_quality_gate(ExportQualityGateRequest(advisor_export_dir=tmp_path))
    markdown = render_export_quality_report(report)

    assert report.status == ExportQualityStatus.PASS_WITH_WARNINGS
    assert len(report.skipped_outputs) == 2
    assert "status: pass-with-warnings" in markdown


def test_export_quality_gate_fails_missing_limitations(tmp_path: Path) -> None:
    _write_minimal_export_dir(tmp_path)
    (tmp_path / "limitations.md").unlink()

    report = run_export_quality_gate(ExportQualityGateRequest(advisor_export_dir=tmp_path))

    assert report.status == ExportQualityStatus.FAIL
    assert any(finding.check_id == "missing-output" for finding in report.findings)
