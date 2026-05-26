from __future__ import annotations

from pathlib import Path

import pytest

from turing_research.pdf.extractors.section_tree import extract_section_tree


def test_section_tree_detects_known_headings(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "sections.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Introduction\nThis is a section.\nResults\nA result.")
    document.save(str(pdf_path))
    document.close()

    nodes, warnings = extract_section_tree(pdf_path)

    assert [node.title for node in nodes] == ["Introduction", "Results"]
    assert nodes[0].evidence_locator == "page:1"
    assert nodes[0].confidence > 0
    assert warnings == []
