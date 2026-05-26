from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pdf_exporter import (
    build_advisor_pdf_export_plan,
    export_advisor_pdf_optional,
)
from turing_research_plus.advisor_export.pptx_exporter import (
    build_advisor_pptx_export_plan,
    export_advisor_pptx_optional,
)
from turing_research_plus.advisor_export.quality_gate import (
    ExportQualityGateRequest,
    ExportQualityStatus,
    run_export_quality_gate,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"
ADVISOR_EXPORT = VGGT / "advisor_export"
DASHBOARD = VGGT / "dashboard_html" / "refined_dashboard.html"


def _fixture_bundle() -> AdvisorMarkdownBundle:
    required = [
        "advisor_report_source.md",
        "slides_outline.md",
        "figure_list.md",
        "table_list.md",
        "evidence_refs.md",
        "limitations.md",
        "next_actions.md",
        "manifest.yaml",
    ]
    return AdvisorMarkdownBundle(
        bundle_id="vggt_advisor_markdown_bundle",
        topic="VGGT / SMPL-X Human Prior",
        output_dir=str(ADVISOR_EXPORT),
        files=[
            AdvisorBundleFile(path=str(ADVISOR_EXPORT / filename), role=filename)
            for filename in required
        ],
    )


def test_v0_7_dashboard_export_chain_with_optional_backends(tmp_path: Path) -> None:
    bundle = _fixture_bundle()
    pdf_plan = build_advisor_pdf_export_plan(bundle, tmp_path / "pdf_export")
    pptx_plan = build_advisor_pptx_export_plan(bundle, tmp_path / "pptx_export")
    pdf_result = export_advisor_pdf_optional(bundle, tmp_path / "pdf_export", force_skip=True)
    pptx_result = export_advisor_pptx_optional(
        bundle,
        tmp_path / "pptx_export",
        force_skip=True,
    )
    quality_report = run_export_quality_gate(
        ExportQualityGateRequest(
            advisor_export_dir=ADVISOR_EXPORT,
            dashboard_paths=[DASHBOARD],
        )
    )
    dashboard_html = DASHBOARD.read_text(encoding="utf-8")

    assert pdf_plan.optional_backend is True
    assert pptx_plan.optional_backend is True
    assert pdf_result.skipped_reason == "PDF backend intentionally skipped"
    assert pptx_result.skipped_reason == "PPTX backend intentionally skipped"
    assert quality_report.status == ExportQualityStatus.PASS_WITH_WARNINGS
    assert "limitations" in (ADVISOR_EXPORT / "limitations.md").read_text(encoding="utf-8").lower()
    assert "refined_dashboard.html" in str(DASHBOARD)
    assert "SAFE DEMO MODE" in dashboard_html
    assert "Not an experiment result" in dashboard_html


def test_v0_7_dashboard_export_fixture_has_no_blocking_quality_findings() -> None:
    report = (ADVISOR_EXPORT / "export_quality_report.md").read_text(encoding="utf-8")

    assert "status: pass-with-warnings" in report
    assert "Findings" in report
    assert "- none" in report
    assert "PDF backend intentionally skipped" in report
    assert "PPTX backend intentionally skipped" in report
