"""Plan-only Advisor PPTX export support."""

from __future__ import annotations

from turing_research_plus.advisor_export.models import (
    AdvisorMarkdownBundle,
    AdvisorPptxExportPlan,
    AdvisorPptxSlidePlan,
)


def build_pptx_export_plan(bundle: AdvisorMarkdownBundle) -> AdvisorPptxExportPlan:
    """Build a conservative PPTX outline from a Markdown bundle."""

    slides = [
        AdvisorPptxSlidePlan(
            slide_id="slide-01",
            title="North Star",
            source_sections=["advisor_report_source.md"],
            evidence_refs=["evidence_refs.md"],
            notes=["Frame the project goal without claiming experimental success."],
        ),
        AdvisorPptxSlidePlan(
            slide_id="slide-02",
            title="Current Evidence State",
            source_sections=["advisor_report_source.md", "evidence_refs.md"],
            evidence_refs=["evidence_refs.md"],
            notes=["Separate observed, planned, blocked, and not-enough-evidence states."],
        ),
        AdvisorPptxSlidePlan(
            slide_id="slide-03",
            title="Artifact and Visual Readiness",
            source_sections=["figure_list.md", "table_list.md", "limitations.md"],
            evidence_refs=["evidence_refs.md"],
            notes=["Do not invent figures or visual boards."],
        ),
        AdvisorPptxSlidePlan(
            slide_id="slide-04",
            title="Failure Modes and Hard Gates",
            source_sections=["advisor_report_source.md", "limitations.md"],
            evidence_refs=["evidence_refs.md"],
            notes=["Keep failure categories tied to existing evidence refs or review flags."],
        ),
        AdvisorPptxSlidePlan(
            slide_id="slide-05",
            title="Related Work and Method Notes",
            source_sections=["advisor_report_source.md", "table_list.md"],
            evidence_refs=["evidence_refs.md"],
            notes=["Keep paper positioning conservative and review-required."],
        ),
        AdvisorPptxSlidePlan(
            slide_id="slide-06",
            title="Next Actions",
            source_sections=["next_actions.md"],
            evidence_refs=[],
            notes=["Call out advisor-facing actions and unresolved blockers."],
        ),
    ]
    return AdvisorPptxExportPlan(
        plan_id=f"{bundle.bundle_id}_pptx_plan",
        source_bundle_id=bundle.bundle_id,
        deck_title=f"{bundle.topic} Advisor PPTX Outline",
        slides=slides,
        safety_warnings=[
            "Plan only: no PPTX file was generated.",
            "No external office tool was called.",
            "Do not fabricate charts, screenshots, or result slides.",
            "Preserve limitations and requires-human-review markers.",
        ],
        limitations=[
            "Binary PPTX export remains an optional future adapter.",
            "Slide content is mapped from Markdown bundle source files.",
            "The outline is not final advisor delivery without review.",
        ],
    )


def render_pptx_outline(plan: AdvisorPptxExportPlan) -> str:
    """Render a PPTX outline as Markdown."""

    lines = [
        "# Advisor PPTX Outline",
        "",
        f"- Plan ID: `{plan.plan_id}`",
        f"- Source bundle: `{plan.source_bundle_id}`",
        f"- Deck title: {plan.deck_title}",
        f"- Template: `{plan.template_name}`",
        f"- Adapter status: `{plan.adapter_status}`",
        "- Generated PPTX: `false`",
        "- External converter called: `false`",
        "- Requires human review: `true`",
        "",
        "## Slides",
        "",
    ]
    for slide in plan.slides:
        lines.extend(
            [
                f"### {slide.slide_id}: {slide.title}",
                "",
                "Source sections:",
                *[f"- `{item}`" for item in slide.source_sections],
                "",
                "Evidence refs:",
                *([f"- `{item}`" for item in slide.evidence_refs] or ["- none"]),
                "",
                "Notes:",
                *[f"- {item}" for item in slide.notes],
                "",
            ]
        )
    lines.extend(["## Safety Warnings", ""])
    lines.extend([f"- {item}" for item in plan.safety_warnings])
    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {item}" for item in plan.limitations])
    lines.append("")
    return "\n".join(lines)


def render_slide_section_mapping(plan: AdvisorPptxExportPlan) -> str:
    """Render slide-to-source mapping as Markdown."""

    lines = [
        "# Slide Section Mapping",
        "",
        "| Slide | Title | Source Sections | Evidence Refs |",
        "| --- | --- | --- | --- |",
    ]
    for slide in plan.slides:
        sources = ", ".join(f"`{item}`" for item in slide.source_sections)
        refs = ", ".join(f"`{item}`" for item in slide.evidence_refs) or "none"
        lines.append(f"| `{slide.slide_id}` | {slide.title} | {sources} | {refs} |")
    lines.extend(
        [
            "",
            "Boundary: this mapping is plan-only. No PPTX file was generated.",
            "",
        ]
    )
    return "\n".join(lines)
