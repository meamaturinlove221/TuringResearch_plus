from __future__ import annotations

from pathlib import Path

import pytest

from turing_research.pdf.asset_report import extract_pdf_assets


def test_pdf_asset_report_serializes_markdown(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "asset_report.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Introduction\n| Metric | Value |\n| Loss | 0.25 |")
    document.save(str(pdf_path))
    document.close()

    report = extract_pdf_assets(pdf_path, tmp_path / "assets")
    markdown = report.to_markdown()

    assert report.source_pdf == pdf_path
    assert report.page_map
    assert report.section_tree
    assert report.extracted_tables
    assert 0 <= report.quality_score <= 1
    assert "# PDF Asset Extraction Report" in markdown
