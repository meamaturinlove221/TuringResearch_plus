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
from turing_research_plus.advisor_export.pdf_models import AdvisorPdfExportStatus


def _bundle(tmp_path: Path) -> AdvisorMarkdownBundle:
    files = [
        "advisor_report_source.md",
        "slides_outline.md",
        "figure_list.md",
        "table_list.md",
        "evidence_refs.md",
        "limitations.md",
        "next_actions.md",
        "manifest.yaml",
    ]
    for filename in files:
        (tmp_path / filename).write_text(
            f"# {filename}\n\nRequires human review.\n",
            encoding="utf-8",
        )
    return AdvisorMarkdownBundle(
        bundle_id="bundle-1",
        topic="VGGT Advisor",
        output_dir=str(tmp_path),
        files=[
            AdvisorBundleFile(path=str(tmp_path / filename), role=filename)
            for filename in files
        ],
    )


def test_build_real_pdf_export_plan_is_optional(tmp_path: Path) -> None:
    plan = build_advisor_pdf_export_plan(_bundle(tmp_path), tmp_path / "pdf")

    assert plan.source_bundle_id == "bundle-1"
    assert plan.output_filename == "advisor_report.pdf"
    assert plan.optional_backend is True
    assert "No charts" in " ".join(plan.safety_warnings)


def test_pdf_export_gracefully_skips_when_forced(tmp_path: Path) -> None:
    result = export_advisor_pdf_optional(_bundle(tmp_path), tmp_path / "pdf", force_skip=True)

    assert result.status == AdvisorPdfExportStatus.SKIPPED
    assert result.output_pdf is None
    assert result.skipped_reason == "PDF backend intentionally skipped"
    assert (tmp_path / "pdf" / "advisor_pdf_review_source.md").exists()
