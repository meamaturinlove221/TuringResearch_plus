"""Export planning for future Advisor Pack binary formats."""

from __future__ import annotations

from turing_research_plus.advisor_export.models import (
    AdvisorExportFormat,
    AdvisorExportPlan,
    AdvisorMarkdownBundle,
)


def build_advisor_export_plan(bundle: AdvisorMarkdownBundle) -> AdvisorExportPlan:
    """Build a conservative export plan from a Markdown bundle."""

    return AdvisorExportPlan(
        plan_id=f"{bundle.bundle_id}_export_plan",
        source_bundle_id=bundle.bundle_id,
        target_formats=[
            AdvisorExportFormat.PDF,
            AdvisorExportFormat.PPTX,
            AdvisorExportFormat.DOCX,
            AdvisorExportFormat.HTML,
        ],
        conversion_tools=[
            "future markdown-to-pdf converter",
            "future markdown-to-pptx converter",
            "future markdown-to-docx converter",
            "future static-html renderer",
        ],
        safety_requirements=[
            "Do not generate charts without source artifacts.",
            "Do not write planned work as observed evidence.",
            "Do not claim SparseConv3D success without evidence ledger support.",
            "Preserve limitations and human-review markers in every export.",
        ],
        non_goals=[
            "No PDF generation in Round 88.",
            "No PPTX generation in Round 88.",
            "No external converter calls in Round 88.",
            "No fabricated figures or tables.",
        ],
        implementation_status="markdown-source-ready",
    )
