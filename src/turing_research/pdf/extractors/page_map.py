"""Lightweight page map extraction for local PDFs."""

from __future__ import annotations

from pathlib import Path

from turing_research.pdf.asset_report import PDFAssetPageMapEntry


def build_page_map(pdf_path: Path) -> tuple[list[PDFAssetPageMapEntry], list[str]]:
    """Build a page-level provenance map without OCR or external services."""

    try:
        import fitz  # type: ignore[import-untyped]
    except ModuleNotFoundError:
        return [], ["PyMuPDF is not installed; page map extraction skipped."]

    entries: list[PDFAssetPageMapEntry] = []
    warnings: list[str] = []
    try:
        document = fitz.open(str(pdf_path))
    except Exception as exc:
        return [], [f"Could not open PDF for page map extraction: {exc}"]

    try:
        for index, page in enumerate(document, start=1):
            rect = page.rect
            text = page.get_text("text") or ""
            images = page.get_images(full=True)
            entries.append(
                PDFAssetPageMapEntry(
                    page_number=index,
                    width=float(rect.width),
                    height=float(rect.height),
                    text_chars=len(text),
                    image_count=len(images),
                )
            )
            if not text.strip():
                warnings.append(f"Page {index} has no extractable text.")
    finally:
        document.close()
    return entries, warnings
