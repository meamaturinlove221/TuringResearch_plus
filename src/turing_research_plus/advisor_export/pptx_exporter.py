"""Optional Advisor PPTX exporter."""

from __future__ import annotations

import importlib.util
from importlib import import_module
from pathlib import Path
from typing import Any

from turing_research_plus.advisor_export.models import AdvisorMarkdownBundle
from turing_research_plus.advisor_export.pptx_models import (
    AdvisorPptxBackend,
    AdvisorPptxExportResult,
    AdvisorPptxExportStatus,
    AdvisorRealPptxExportPlan,
)
from turing_research_plus.advisor_export.pptx_templates import (
    build_advisor_pptx_slides,
    render_pptx_review_markdown,
)


def build_advisor_pptx_export_plan(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    output_filename: str = "advisor_deck.pptx",
) -> AdvisorRealPptxExportPlan:
    """Build a concrete optional PPTX export plan."""

    return AdvisorRealPptxExportPlan(
        plan_id=f"{bundle.bundle_id}_real_pptx_export",
        source_bundle_id=bundle.bundle_id,
        output_dir=str(output_dir),
        output_filename=output_filename,
        deck_title=f"{bundle.topic} Advisor Deck",
        slides=build_advisor_pptx_slides(bundle),
        safety_warnings=[
            "PPTX export is optional and skipped when backend dependencies are missing.",
            "Deck content is derived from AdvisorMarkdownBundle source files.",
            "No fake charts, visual evidence, or experiment values are generated.",
            "Not-ready claims remain explicitly marked.",
            "Planned work remains planned and is not observed evidence.",
        ],
        limitations=[
            "The generated deck, when available, is a review artifact only.",
            "The Markdown bundle remains the authoritative source package.",
            "Human review is required before advisor delivery.",
        ],
    )


def export_advisor_pptx_optional(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    output_filename: str = "advisor_deck.pptx",
    force_skip: bool = False,
    write_review_source: bool = True,
) -> AdvisorPptxExportResult:
    """Optionally export a PPTX deck, returning skipped when backend is unavailable."""

    plan = build_advisor_pptx_export_plan(bundle, output_dir, output_filename=output_filename)
    output_dir.mkdir(parents=True, exist_ok=True)
    review_source = output_dir / "advisor_pptx_review_source.md"
    if write_review_source:
        review_source.write_text(render_pptx_review_markdown(bundle), encoding="utf-8")

    generated_files = [str(review_source)] if write_review_source else []
    if force_skip or not _python_pptx_available():
        reason = "python-pptx backend is not installed"
        if force_skip:
            reason = "PPTX backend intentionally skipped"
        return AdvisorPptxExportResult(
            plan_id=plan.plan_id,
            source_bundle_id=plan.source_bundle_id,
            status=AdvisorPptxExportStatus.SKIPPED,
            backend=AdvisorPptxBackend.PYTHON_PPTX,
            skipped_reason=reason,
            generated_files=generated_files,
            warnings=[
                "Optional PPTX export skipped without failing default tests.",
                "Use the Markdown review source as the audit artifact.",
            ],
        )

    pptx_path = output_dir / output_filename
    _write_python_pptx(plan, pptx_path)
    generated_files.append(str(pptx_path))
    return AdvisorPptxExportResult(
        plan_id=plan.plan_id,
        source_bundle_id=plan.source_bundle_id,
        status=AdvisorPptxExportStatus.GENERATED,
        backend=AdvisorPptxBackend.PYTHON_PPTX,
        output_pptx=str(pptx_path),
        generated_files=generated_files,
        warnings=[
            "PPTX was generated from reviewed Markdown source.",
            "PPTX is not new evidence and requires human review.",
        ],
    )


def _python_pptx_available() -> bool:
    return importlib.util.find_spec("pptx") is not None


def _write_python_pptx(plan: AdvisorRealPptxExportPlan, output_path: Path) -> None:
    presentation_module: Any = import_module("pptx")
    presentation = presentation_module.Presentation()

    title_slide_layout = presentation.slide_layouts[0]
    title_slide = presentation.slides.add_slide(title_slide_layout)
    title_slide.shapes.title.text = plan.deck_title
    title_slide.placeholders[1].text = "Review deck / requires human review"

    bullet_layout = presentation.slide_layouts[1]
    for slide_spec in plan.slides:
        slide = presentation.slides.add_slide(bullet_layout)
        slide.shapes.title.text = slide_spec.title
        body = slide.placeholders[1].text_frame
        body.clear()
        for index, bullet in enumerate(slide_spec.bullets):
            paragraph = body.paragraphs[0] if index == 0 else body.add_paragraph()
            marker = "[NOT-READY] " if slide_spec.not_ready and index == 0 else ""
            paragraph.text = f"{marker}{bullet}"
            paragraph.level = 0

    presentation.save(str(output_path))
