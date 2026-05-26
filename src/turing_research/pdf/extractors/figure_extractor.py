"""Lightweight figure extraction for local PDFs."""

from __future__ import annotations

from hashlib import sha256
from pathlib import Path
from typing import Any

from turing_research.pdf.asset_report import (
    PDFBoundingBox,
    PDFExtractedFigure,
    PDFExtractionStatus,
)


def extract_figures(
    pdf_path: Path,
    output_dir: Path | None = None,
) -> tuple[list[PDFExtractedFigure], list[str]]:
    """Extract embedded images as lightweight figure assets when PyMuPDF is available."""

    try:
        import fitz  # type: ignore[import-untyped]
    except ModuleNotFoundError:
        return [], ["PyMuPDF is not installed; figure extraction skipped."]

    figures: list[PDFExtractedFigure] = []
    warnings: list[str] = []
    if output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        document = fitz.open(str(pdf_path))
    except Exception as exc:
        return [], [f"Could not open PDF for figure extraction: {exc}"]

    source_hash = _source_hash(pdf_path)
    try:
        for page_index, page in enumerate(document, start=1):
            images = page.get_images(full=True)
            if not images:
                continue
            for image_index, image in enumerate(images, start=1):
                xref = image[0]
                figure_id = f"fig-{source_hash}-p{page_index}-{image_index}"
                output_path: Path | None = None
                item_warnings: list[str] = []
                if output_dir is not None:
                    try:
                        image_payload = document.extract_image(xref)
                        ext = image_payload.get("ext", "png")
                        output_path = output_dir / f"{figure_id}.{ext}"
                        output_path.write_bytes(image_payload["image"])
                    except Exception as exc:
                        item_warnings.append(f"Could not write extracted image: {exc}")
                figures.append(
                    PDFExtractedFigure(
                        figure_id=figure_id,
                        source_pdf=pdf_path,
                        page_number=page_index,
                        bbox=_image_bbox(page, xref),
                        output_path=output_path,
                        caption=None,
                        extraction_status=PDFExtractionStatus.EXTRACTED,
                        warnings=item_warnings,
                    )
                )
    finally:
        document.close()

    if not figures:
        warnings.append("No embedded figures were found.")
    return figures, warnings


def _source_hash(pdf_path: Path) -> str:
    return sha256(str(pdf_path.resolve()).encode("utf-8")).hexdigest()[:10]


def _image_bbox(page: Any, xref: int) -> PDFBoundingBox | None:
    rects = page.get_image_rects(xref)
    if not rects:
        return None
    rect = rects[0]
    return PDFBoundingBox(
        x0=float(rect.x0),
        y0=float(rect.y0),
        x1=float(rect.x1),
        y1=float(rect.y1),
    )
