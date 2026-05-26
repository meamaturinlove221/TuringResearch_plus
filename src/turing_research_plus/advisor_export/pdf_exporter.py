"""Optional Advisor PDF exporter."""

from __future__ import annotations

import importlib.util
from importlib import import_module
from pathlib import Path
from textwrap import wrap
from typing import Any

from turing_research_plus.advisor_export.models import AdvisorMarkdownBundle
from turing_research_plus.advisor_export.pdf_models import (
    AdvisorPdfBackend,
    AdvisorPdfExportResult,
    AdvisorPdfExportStatus,
    AdvisorRealPdfExportPlan,
)
from turing_research_plus.advisor_export.pdf_templates import (
    PDF_REQUIRED_SECTIONS,
    build_pdf_section_text,
    render_pdf_review_markdown,
)


def build_advisor_pdf_export_plan(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    output_filename: str = "advisor_report.pdf",
) -> AdvisorRealPdfExportPlan:
    """Build a concrete optional PDF export plan."""

    return AdvisorRealPdfExportPlan(
        plan_id=f"{bundle.bundle_id}_real_pdf_export",
        source_bundle_id=bundle.bundle_id,
        output_dir=str(output_dir),
        output_filename=output_filename,
        title=f"{bundle.topic} Advisor Report",
        sections=PDF_REQUIRED_SECTIONS,
        source_files=[Path(item.path).name for item in bundle.files],
        safety_warnings=[
            "PDF export is optional and skipped when backend dependencies are missing.",
            "PDF content is derived from AdvisorMarkdownBundle source files.",
            "No charts, visual evidence, or experiment values are fabricated.",
            "Planned work remains planned and is not observed evidence.",
        ],
        limitations=[
            "The generated PDF, when available, is a review artifact only.",
            "The Markdown bundle remains the authoritative source package.",
            "Human review is required before advisor delivery.",
        ],
    )


def export_advisor_pdf_optional(
    bundle: AdvisorMarkdownBundle,
    output_dir: Path,
    *,
    output_filename: str = "advisor_report.pdf",
    force_skip: bool = False,
    write_review_source: bool = True,
) -> AdvisorPdfExportResult:
    """Optionally export a PDF, returning skipped when the backend is unavailable."""

    plan = build_advisor_pdf_export_plan(bundle, output_dir, output_filename=output_filename)
    output_dir.mkdir(parents=True, exist_ok=True)
    review_source = output_dir / "advisor_pdf_review_source.md"
    if write_review_source:
        review_source.write_text(render_pdf_review_markdown(bundle), encoding="utf-8")

    generated_files = [str(review_source)] if write_review_source else []
    if force_skip or not _reportlab_available():
        reason = "reportlab backend is not installed"
        if force_skip:
            reason = "PDF backend intentionally skipped"
        return AdvisorPdfExportResult(
            plan_id=plan.plan_id,
            source_bundle_id=plan.source_bundle_id,
            status=AdvisorPdfExportStatus.SKIPPED,
            backend=AdvisorPdfBackend.REPORTLAB,
            skipped_reason=reason,
            generated_files=generated_files,
            warnings=[
                "Optional PDF export skipped without failing default tests.",
                "Use the Markdown review source as the audit artifact.",
            ],
        )

    pdf_path = output_dir / output_filename
    _write_reportlab_pdf(plan, bundle, pdf_path)
    generated_files.append(str(pdf_path))
    return AdvisorPdfExportResult(
        plan_id=plan.plan_id,
        source_bundle_id=plan.source_bundle_id,
        status=AdvisorPdfExportStatus.GENERATED,
        backend=AdvisorPdfBackend.REPORTLAB,
        output_pdf=str(pdf_path),
        generated_files=generated_files,
        warnings=[
            "PDF was generated from reviewed Markdown source.",
            "PDF is not new evidence and requires human review.",
        ],
    )


def _reportlab_available() -> bool:
    return importlib.util.find_spec("reportlab") is not None


def _write_reportlab_pdf(
    plan: AdvisorRealPdfExportPlan,
    bundle: AdvisorMarkdownBundle,
    output_path: Path,
) -> None:
    pagesizes: Any = import_module("reportlab.lib.pagesizes")
    canvas_module: Any = import_module("reportlab.pdfgen.canvas")
    letter = pagesizes.letter

    sections = build_pdf_section_text(bundle)
    pdf = canvas_module.Canvas(str(output_path), pagesize=letter)
    width, height = letter
    margin = 54
    y = height - margin

    def draw_line(text: str, *, font: str = "Helvetica", size: int = 10) -> None:
        nonlocal y
        if y < margin:
            pdf.showPage()
            y = height - margin
        pdf.setFont(font, size)
        pdf.drawString(margin, y, text[:110])
        y -= size + 5

    draw_line(plan.title, font="Helvetica-Bold", size=15)
    draw_line("Status: review PDF / requires human review", font="Helvetica-Bold", size=10)
    draw_line("Boundary: no fabricated figures, tables, or experiment results.", size=9)
    y -= 8

    for section in plan.sections:
        draw_line(section.title(), font="Helvetica-Bold", size=12)
        text = sections.get(section, "")
        for paragraph in text.splitlines() or ["No source text provided."]:
            line = paragraph.strip()
            if not line:
                y -= 5
                continue
            for wrapped in wrap(line, width=92):
                draw_line(wrapped, size=9)
        y -= 6

    pdf.save()
