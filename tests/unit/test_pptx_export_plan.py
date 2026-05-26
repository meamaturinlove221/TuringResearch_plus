from __future__ import annotations

import pytest

from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorMarkdownBundle,
    AdvisorPptxExportPlan,
)
from turing_research_plus.advisor_export.pptx_plan import (
    build_pptx_export_plan,
    render_pptx_outline,
    render_slide_section_mapping,
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


def test_pptx_export_plan_is_plan_only() -> None:
    plan = build_pptx_export_plan(_bundle())
    outline = render_pptx_outline(plan)
    mapping = render_slide_section_mapping(plan)

    assert plan.generated_pptx is False
    assert plan.external_converter_called is False
    assert len(plan.slides) >= 6
    assert "Generated PPTX: `false`" in outline
    assert "No PPTX file was generated" in mapping


def test_pptx_export_plan_rejects_generated_pptx_claim() -> None:
    with pytest.raises(ValueError, match="must not claim generated PPTX"):
        AdvisorPptxExportPlan(
            plan_id="pptx-1",
            source_bundle_id="bundle-1",
            deck_title="Advisor Deck",
            generated_pptx=True,
        )


def test_pptx_export_plan_requires_slides() -> None:
    with pytest.raises(ValueError, match="requires at least one slide"):
        AdvisorPptxExportPlan(
            plan_id="pptx-1",
            source_bundle_id="bundle-1",
            deck_title="Advisor Deck",
        )
