from __future__ import annotations

import pytest

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
    AdvisorPdfExportPlan,
)
from turing_research_plus.advisor_export.pdf_plan import (
    build_pdf_export_plan,
    render_pdf_export_plan,
)


def _bundle() -> AdvisorMarkdownBundle:
    return AdvisorMarkdownBundle(
        bundle_id="bundle-1",
        topic="VGGT",
        output_dir="out",
        files=[
            AdvisorBundleFile(path=f"out/{filename}", role=filename)
            for filename in [
                "advisor_report_source.md",
                "slides_outline.md",
                "figure_list.md",
                "table_list.md",
                "evidence_refs.md",
                "limitations.md",
                "next_actions.md",
                "manifest.yaml",
            ]
        ],
    )


def test_pdf_export_plan_is_plan_only() -> None:
    plan = build_pdf_export_plan(_bundle())
    markdown = render_pdf_export_plan(plan)

    assert plan.generated_pdf is False
    assert plan.external_converter_called is False
    assert plan.adapter_status == "optional_not_run"
    assert "Generated PDF: `false`" in markdown
    assert "No external converter was called" in markdown


def test_pdf_export_plan_rejects_generated_pdf_claim() -> None:
    with pytest.raises(ValueError, match="must not claim generated PDF"):
        AdvisorPdfExportPlan(
            plan_id="pdf-1",
            source_bundle_id="bundle-1",
            document_title="Advisor PDF",
            generated_pdf=True,
        )


def test_pdf_export_plan_rejects_external_converter_claim() -> None:
    with pytest.raises(ValueError, match="must not call external converters"):
        AdvisorPdfExportPlan(
            plan_id="pdf-1",
            source_bundle_id="bundle-1",
            document_title="Advisor PDF",
            external_converter_called=True,
        )
