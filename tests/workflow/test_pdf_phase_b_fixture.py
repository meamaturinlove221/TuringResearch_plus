from __future__ import annotations

import base64
from pathlib import Path

import pytest

from turing_research.pdf.asset_report import extract_pdf_assets

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def test_pdf_phase_b_fixture_extracts_assets(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "phase_b.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Introduction\n| Method | Signal |\n| VGGT | local |")
    page.insert_image(fitz.Rect(72, 140, 92, 160), stream=PNG_1X1)
    document.save(str(pdf_path))
    document.close()

    report = extract_pdf_assets(pdf_path, tmp_path / "assets")

    assert report.extracted_figures
    assert report.extracted_tables
    assert report.page_map
    assert report.section_tree
    assert report.quality_score > 0
    assert report.paper_registry_entries == []
