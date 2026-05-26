"""Plan-only Advisor PDF export support."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.advisor_export.models import (
    AdvisorMarkdownBundle,
    AdvisorPdfExportPlan,
)

PDF_SECTION_ORDER = [
    "Executive Summary",
    "Evidence State",
    "Artifact and Visual Readiness",
    "Run Status and Failure Modes",
    "Related Work / Paper Notes",
    "Limitations",
    "Next Actions",
]


def build_pdf_export_plan(bundle: AdvisorMarkdownBundle) -> AdvisorPdfExportPlan:
    """Build a conservative PDF export plan from a Markdown bundle."""

    source_files = [Path(item.path).name for item in bundle.files]
    return AdvisorPdfExportPlan(
        plan_id=f"{bundle.bundle_id}_pdf_plan",
        source_bundle_id=bundle.bundle_id,
        document_title=f"{bundle.topic} Advisor PDF Export Plan",
        source_files=source_files,
        section_order=PDF_SECTION_ORDER,
        safety_warnings=[
            "Plan only: no PDF file was generated.",
            "No external converter was called.",
            "Do not fabricate figures, tables, or experiment results.",
            "Preserve limitations and human-review markers.",
        ],
        limitations=[
            "Binary PDF export remains an optional future adapter.",
            "The plan depends on existing Markdown source files.",
            "Planned work must not be written as observed evidence.",
        ],
    )


def render_pdf_export_plan(plan: AdvisorPdfExportPlan) -> str:
    """Render a PDF export plan as Markdown."""

    lines = [
        "# Advisor PDF Export Plan",
        "",
        f"- Plan ID: `{plan.plan_id}`",
        f"- Source bundle: `{plan.source_bundle_id}`",
        f"- Document title: {plan.document_title}",
        f"- Template: `{plan.template_name}`",
        f"- Adapter status: `{plan.adapter_status}`",
        "- Generated PDF: `false`",
        "- External converter called: `false`",
        "- Requires human review: `true`",
        "",
        "## Source Files",
        "",
    ]
    lines.extend([f"- `{item}`" for item in plan.source_files])
    lines.extend(["", "## Section Order", ""])
    lines.extend([f"{index}. {section}" for index, section in enumerate(plan.section_order, 1)])
    lines.extend(["", "## Safety Warnings", ""])
    lines.extend([f"- {item}" for item in plan.safety_warnings])
    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {item}" for item in plan.limitations])
    lines.append("")
    return "\n".join(lines)
