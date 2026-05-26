"""PDF Phase B asset extraction report models."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PDFExtractionStatus(StrEnum):
    """Status for a lightweight PDF asset extraction item."""

    EXTRACTED = "extracted"
    NOT_FOUND = "not_found"
    SKIPPED = "skipped"
    ERROR = "error"


class PDFBoundingBox(BaseModel):
    """Optional PDF bounding box coordinates."""

    model_config = ConfigDict(extra="forbid")

    x0: float
    y0: float
    x1: float
    y1: float


class PDFExtractedFigure(BaseModel):
    """One extracted or discovered PDF figure asset."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str = Field(min_length=1)
    source_pdf: Path
    page_number: int = Field(ge=1)
    bbox: PDFBoundingBox | None = None
    output_path: Path | None = None
    caption: str | None = None
    extraction_status: PDFExtractionStatus
    warnings: list[str] = Field(default_factory=list)


class PDFExtractedTable(BaseModel):
    """One lightweight extracted PDF table asset."""

    model_config = ConfigDict(extra="forbid")

    table_id: str = Field(min_length=1)
    source_pdf: Path
    page_number: int = Field(ge=1)
    extraction_format: str = Field(min_length=1)
    output_path: Path | None = None
    markdown_table: str | None = None
    extraction_status: PDFExtractionStatus
    warnings: list[str] = Field(default_factory=list)


class PDFAssetPageMapEntry(BaseModel):
    """Page-level provenance map for Phase B extraction."""

    model_config = ConfigDict(extra="forbid")

    page_number: int = Field(ge=1)
    width: float = Field(gt=0)
    height: float = Field(gt=0)
    text_chars: int = Field(ge=0)
    image_count: int = Field(ge=0)


class PDFSectionNode(BaseModel):
    """Lightweight section tree node."""

    model_config = ConfigDict(extra="forbid")

    section_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    level: int = Field(ge=1)
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    parent_section_id: str | None = None
    child_section_ids: list[str] = Field(default_factory=list)
    evidence_locator: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


class PDFAssetExtractionReport(BaseModel):
    """Phase B PDF figure/table/section/page-map extraction report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(min_length=1)
    source_pdf: Path
    extracted_figures: list[PDFExtractedFigure] = Field(default_factory=list)
    extracted_tables: list[PDFExtractedTable] = Field(default_factory=list)
    page_map: list[PDFAssetPageMapEntry] = Field(default_factory=list)
    section_tree: list[PDFSectionNode] = Field(default_factory=list)
    extraction_warnings: list[str] = Field(default_factory=list)
    quality_score: float = Field(ge=0.0, le=1.0)
    paper_registry_entries: list[dict[str, Any]] = Field(default_factory=list)

    def to_markdown(self) -> str:
        """Serialize the report to a compact Markdown summary."""

        lines = [
            f"# PDF Asset Extraction Report: {self.report_id}",
            "",
            f"- Source PDF: `{self.source_pdf}`",
            f"- Quality score: {self.quality_score:.2f}",
            "",
            "## Figures",
            "",
        ]
        if self.extracted_figures:
            lines.extend(
                f"- {figure.figure_id}: page {figure.page_number}, "
                f"status {figure.extraction_status.value}"
                for figure in self.extracted_figures
            )
        else:
            lines.append("- No figures extracted.")
        lines.extend(["", "## Tables", ""])
        if self.extracted_tables:
            lines.extend(
                f"- {table.table_id}: page {table.page_number}, "
                f"status {table.extraction_status.value}"
                for table in self.extracted_tables
            )
        else:
            lines.append("- No tables extracted.")
        if self.extraction_warnings:
            lines.extend(["", "## Warnings", ""])
            lines.extend(f"- {warning}" for warning in self.extraction_warnings)
        return "\n".join(lines) + "\n"


def extract_pdf_assets(
    pdf_path: Path,
    output_dir: Path | None = None,
) -> PDFAssetExtractionReport:
    """Build a lightweight Phase B asset extraction report for one local PDF."""

    from turing_research.pdf.extractors.figure_extractor import extract_figures
    from turing_research.pdf.extractors.page_map import build_page_map
    from turing_research.pdf.extractors.section_tree import extract_section_tree
    from turing_research.pdf.extractors.table_extractor import extract_tables

    warnings: list[str] = []
    figures, figure_warnings = extract_figures(
        pdf_path,
        None if output_dir is None else output_dir / "figures",
    )
    tables, table_warnings = extract_tables(
        pdf_path,
        None if output_dir is None else output_dir / "tables",
    )
    page_map, page_warnings = build_page_map(pdf_path)
    section_tree, section_warnings = extract_section_tree(pdf_path)
    warnings.extend(figure_warnings)
    warnings.extend(table_warnings)
    warnings.extend(page_warnings)
    warnings.extend(section_warnings)
    return PDFAssetExtractionReport(
        report_id=f"{pdf_path.stem}-pdf-phase-b-assets",
        source_pdf=pdf_path,
        extracted_figures=figures,
        extracted_tables=tables,
        page_map=page_map,
        section_tree=section_tree,
        extraction_warnings=list(dict.fromkeys(warnings)),
        quality_score=_quality_score(figures, tables, page_map, section_tree, warnings),
        paper_registry_entries=[],
    )


def _quality_score(
    figures: list[PDFExtractedFigure],
    tables: list[PDFExtractedTable],
    page_map: list[PDFAssetPageMapEntry],
    section_tree: list[PDFSectionNode],
    warnings: list[str],
) -> float:
    score = 0.45
    if page_map:
        score += 0.2
    if section_tree:
        score += 0.15
    if figures:
        score += 0.1
    if tables:
        score += 0.1
    score -= min(len(warnings) * 0.04, 0.25)
    return max(0.0, min(1.0, score))
