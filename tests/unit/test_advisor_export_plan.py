from __future__ import annotations

from turing_research_plus.advisor_export.export_plan import build_advisor_export_plan
from turing_research_plus.advisor_export.models import (
    AdvisorBundleFile,
    AdvisorExportFormat,
    AdvisorMarkdownBundle,
)


def test_advisor_export_plan_is_future_only() -> None:
    bundle = AdvisorMarkdownBundle(
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

    plan = build_advisor_export_plan(bundle)

    assert plan.source_bundle_id == "bundle-1"
    assert AdvisorExportFormat.PDF in plan.target_formats
    assert AdvisorExportFormat.PPTX in plan.target_formats
    assert plan.implementation_status == "markdown-source-ready"
    assert any("No PDF generation" in item for item in plan.non_goals)
