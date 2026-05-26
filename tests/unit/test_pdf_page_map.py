from __future__ import annotations

from pathlib import Path

import pytest

from turing_research.pdf.extractors.page_map import build_page_map


def test_page_map_records_page_metadata(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "pages.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Introduction\nPage map fixture.")
    document.save(str(pdf_path))
    document.close()

    page_map, warnings = build_page_map(pdf_path)

    assert len(page_map) == 1
    assert page_map[0].page_number == 1
    assert page_map[0].width > 0
    assert page_map[0].height > 0
    assert page_map[0].text_chars > 0
    assert warnings == []
