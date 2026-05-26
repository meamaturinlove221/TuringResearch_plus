from __future__ import annotations

import base64
from pathlib import Path

import pytest

from turing_research.pdf.asset_report import extract_pdf_assets
from turing_research_plus.paper.figure_registry import FigureAssetKind, FigureAssetStatus
from turing_research_plus.paper.pdf_asset_import import register_pdf_assets

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


def test_pdf_assets_register_to_paper_registry(tmp_path: Path) -> None:
    fitz = pytest.importorskip("fitz")
    pdf_path = tmp_path / "paper_assets.pdf"
    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), "Methods\n| Part | Role |\n| Figure | Evidence |")
    page.insert_image(fitz.Rect(72, 140, 92, 160), stream=PNG_1X1)
    document.save(str(pdf_path))
    document.close()

    report = extract_pdf_assets(pdf_path, tmp_path / "assets")
    registry, outputs = register_pdf_assets(report, used_in_blocks=["related_work"])

    assert outputs
    assert len(registry.assets) == len(report.extracted_figures) + len(report.extracted_tables)
    assert all(asset.status == FigureAssetStatus.READY for asset in registry.assets)
    assert any(
        asset.asset_kind == FigureAssetKind.PDF_EXTRACTED_FIGURE for asset in registry.assets
    )
    assert any(
        asset.asset_kind == FigureAssetKind.PDF_EXTRACTED_TABLE for asset in registry.assets
    )
