"""Import PDF Phase B assets into the paper figure registry."""

from __future__ import annotations

from turing_research.pdf.asset_report import PDFAssetExtractionReport
from turing_research_plus.paper.figure_registry import (
    FigureAssetKind,
    FigureAssetRegistry,
    FigureRegisterInput,
    FigureRegisterOutput,
    register_figure,
)


def register_pdf_assets(
    report: PDFAssetExtractionReport,
    used_in_blocks: list[str] | None = None,
    registry: FigureAssetRegistry | None = None,
) -> tuple[FigureAssetRegistry, list[FigureRegisterOutput]]:
    """Register extracted PDF figures and tables as paper assets."""

    current = registry or FigureAssetRegistry()
    outputs: list[FigureRegisterOutput] = []
    blocks = used_in_blocks or ["related_work"]

    for figure in report.extracted_figures:
        result = register_figure(
            FigureRegisterInput(
                figure_id=figure.figure_id,
                title=f"PDF figure from page {figure.page_number}",
                source_file=figure.output_path or report.source_pdf,
                caption=figure.caption or f"Extracted figure from page {figure.page_number}.",
                used_in_blocks=blocks,
                asset_kind=FigureAssetKind.PDF_EXTRACTED_FIGURE,
                original_pdf_source=report.source_pdf,
            ),
            registry=current,
        )
        current = result.registry
        outputs.append(result)

    for table in report.extracted_tables:
        result = register_figure(
            FigureRegisterInput(
                figure_id=table.table_id,
                title=f"PDF table from page {table.page_number}",
                source_file=table.output_path or report.source_pdf,
                caption=f"Extracted table from page {table.page_number}.",
                used_in_blocks=blocks,
                asset_kind=FigureAssetKind.PDF_EXTRACTED_TABLE,
                original_pdf_source=report.source_pdf,
            ),
            registry=current,
        )
        current = result.registry
        outputs.append(result)

    return current, outputs
