from __future__ import annotations

from pathlib import Path

import pytest

from turing_research.pdf.asset_report import PDFExtractionStatus
from turing_research.pdf.extractors.table_extractor import extract_tables


def create_pdf_with_table(path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Results\n| Metric | Value |\n| Accuracy | 0.75 |")
    document.save(str(path))
    document.close()


def test_extract_tables_from_pipe_text(tmp_path: Path) -> None:
    pdf_path = tmp_path / "table.pdf"
    create_pdf_with_table(pdf_path)

    tables, warnings = extract_tables(pdf_path, tmp_path / "tables")

    assert len(tables) == 1
    assert tables[0].source_pdf == pdf_path
    assert tables[0].page_number == 1
    assert tables[0].markdown_table is not None
    assert "| Metric | Value |" in tables[0].markdown_table
    assert tables[0].output_path is not None
    assert tables[0].output_path.exists()
    assert tables[0].extraction_status == PDFExtractionStatus.EXTRACTED
    assert warnings == []


def test_extract_tables_without_table_warns(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "no_table.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "No table here.")
    document.save(str(pdf_path))
    document.close()

    tables, warnings = extract_tables(pdf_path)

    assert tables == []
    assert "No lightweight text tables were found." in warnings
