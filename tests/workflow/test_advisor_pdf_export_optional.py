from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
)
from turing_research_plus.advisor_export.pdf_exporter import export_advisor_pdf_optional
from turing_research_plus.advisor_export.pdf_models import AdvisorPdfExportStatus

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey" / "advisor_export"


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
        output_dir=str(EXAMPLE),
        files=[
            AdvisorBundleFile(path=str(EXAMPLE / filename), role=filename)
            for filename in required
        ],
    )


def test_vggt_advisor_pdf_export_optional_skips_without_backend(tmp_path: Path) -> None:
    result = export_advisor_pdf_optional(_fixture_bundle(), tmp_path, force_skip=True)
    review_source = (tmp_path / "advisor_pdf_review_source.md").read_text(encoding="utf-8")

    assert result.status == AdvisorPdfExportStatus.SKIPPED
    assert result.skipped_reason == "PDF backend intentionally skipped"
    assert "optional PDF export source" in review_source
    assert "No figures, result values, or experiment claims are fabricated" in review_source
    assert "Planned work remains planned" in review_source


def test_committed_pdf_export_fixture_is_skip_safe() -> None:
    output_dir = EXAMPLE / "pdf_export"
    report = (output_dir / "pdf_export_report.md").read_text(encoding="utf-8")
    review_source = (output_dir / "advisor_pdf_review_source.md").read_text(encoding="utf-8")

    assert "status: skipped" in report
    assert "PDF backend intentionally skipped" in report
    assert "requires_human_review: true" in report
    assert "No figures, result values, or experiment claims are fabricated" in review_source
