from __future__ import annotations

import pytest

from turing_research_plus.advisor_export.pptx_models import (
    AdvisorPptxExportResult,
    AdvisorPptxExportStatus,
    AdvisorPptxSlide,
    AdvisorRealPptxExportPlan,
)
from turing_research_plus.advisor_export.pptx_templates import DECK_SECTION_TITLES


def _slides() -> list[AdvisorPptxSlide]:
    return [
        AdvisorPptxSlide(
            slide_id=f"slide-{index:02d}",
            title=title,
            bullets=["not-ready: requires evidence review"],
            not_ready=True,
        )
        for index, title in enumerate(DECK_SECTION_TITLES, 1)
    ]


def test_real_pptx_export_plan_requires_8_sections() -> None:
    plan = AdvisorRealPptxExportPlan(
        plan_id="pptx-1",
        source_bundle_id="bundle-1",
        output_dir="out",
        deck_title="Advisor Deck",
        slides=_slides(),
    )

    assert plan.optional_backend is True
    assert plan.requires_human_review is True
    assert len(plan.slides) == 8


def test_not_ready_slide_requires_marker() -> None:
    with pytest.raises(ValueError, match="not-ready marker"):
        AdvisorPptxSlide(
            slide_id="slide-01",
            title="Visual Readiness",
            bullets=["missing reviewed visual evidence"],
            not_ready=True,
        )


def test_pptx_export_result_requires_skip_reason() -> None:
    with pytest.raises(ValueError, match="skipped PPTX result requires skipped_reason"):
        AdvisorPptxExportResult(
            plan_id="pptx-1",
            source_bundle_id="bundle-1",
            status=AdvisorPptxExportStatus.SKIPPED,
        )
