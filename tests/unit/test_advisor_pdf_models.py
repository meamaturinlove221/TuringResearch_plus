from __future__ import annotations

import pytest

from turing_research_plus.advisor_export.pdf_models import (
    AdvisorPdfExportResult,
    AdvisorPdfExportStatus,
    AdvisorRealPdfExportPlan,
)
from turing_research_plus.advisor_export.pdf_templates import PDF_REQUIRED_SECTIONS


def test_real_pdf_export_plan_requires_review_sections() -> None:
    plan = AdvisorRealPdfExportPlan(
        plan_id="pdf-1",
        source_bundle_id="bundle-1",
        output_dir="out",
        title="Advisor PDF",
        sections=PDF_REQUIRED_SECTIONS,
    )

    assert plan.optional_backend is True
    assert plan.requires_human_review is True
    assert "current status" in plan.sections


def test_real_pdf_export_plan_rejects_non_pdf_filename() -> None:
    with pytest.raises(ValueError, match="must end with .pdf"):
        AdvisorRealPdfExportPlan(
            plan_id="pdf-1",
            source_bundle_id="bundle-1",
            output_dir="out",
            output_filename="advisor_report.txt",
            title="Advisor PDF",
            sections=PDF_REQUIRED_SECTIONS,
        )


def test_pdf_export_result_requires_skip_reason() -> None:
    with pytest.raises(ValueError, match="skipped PDF result requires skipped_reason"):
        AdvisorPdfExportResult(
            plan_id="pdf-1",
            source_bundle_id="bundle-1",
            status=AdvisorPdfExportStatus.SKIPPED,
        )
