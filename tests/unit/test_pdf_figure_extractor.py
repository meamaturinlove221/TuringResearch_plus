from __future__ import annotations

import base64
from pathlib import Path

import pytest

from turing_research.pdf.asset_report import PDFExtractionStatus
from turing_research.pdf.extractors.figure_extractor import extract_figures

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def create_pdf_with_image(path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Figure 1. Tiny test image.")
    page.insert_image(fitz.Rect(72, 100, 92, 120), stream=PNG_1X1)
    document.save(str(path))
    document.close()


def test_extract_figures_from_fixture_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "figure.pdf"
    create_pdf_with_image(pdf_path)

    figures, warnings = extract_figures(pdf_path, tmp_path / "assets")

    assert len(figures) == 1
    assert figures[0].source_pdf == pdf_path
    assert figures[0].page_number == 1
    assert figures[0].output_path is not None
    assert figures[0].output_path.exists()
    assert figures[0].extraction_status == PDFExtractionStatus.EXTRACTED
    assert warnings == []


def test_extract_figures_empty_pdf_warns(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "empty.pdf"
    document = fitz.open()
    document.new_page()
    document.save(str(pdf_path))
    document.close()

    figures, warnings = extract_figures(pdf_path)

    assert figures == []
    assert "No embedded figures were found." in warnings
