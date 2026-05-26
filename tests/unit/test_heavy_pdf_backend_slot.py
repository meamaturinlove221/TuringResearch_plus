from __future__ import annotations

import pytest

from turing_research_plus.scholar_pipeline import (
    HeavyPdfBackendKind,
    HeavyPdfBackendRequest,
    HeavyPdfBackendStatus,
    build_heavy_pdf_backend_slot,
    render_heavy_pdf_backend_slot,
)


def test_heavy_pdf_backend_slot_is_disabled_interface_only() -> None:
    slot = build_heavy_pdf_backend_slot()

    assert slot.backend == HeavyPdfBackendKind.MINERU
    assert slot.status == HeavyPdfBackendStatus.SKIPPED
    assert slot.interface_only is True
    assert slot.implementation_present is False
    assert slot.dependency_required is False
    assert slot.ocr_enabled is False
    assert slot.large_pdf_processing is False
    assert slot.requires_human_review is True
    assert slot.release_blocker is False
    assert "future optional backend" in slot.skipped_reason


def test_heavy_pdf_backend_slot_supports_arxiv2md_future_slot() -> None:
    slot = build_heavy_pdf_backend_slot(
        HeavyPdfBackendRequest(backend=HeavyPdfBackendKind.ARXIV2MD)
    )

    assert slot.backend == HeavyPdfBackendKind.ARXIV2MD
    assert "arxiv2md" in slot.skipped_reason
    assert slot.release_blocker is False


def test_heavy_pdf_backend_slot_rejects_enabled_heavy_behavior() -> None:
    with pytest.raises(ValueError, match="disabled by default"):
        HeavyPdfBackendRequest(enabled=True)
    with pytest.raises(ValueError, match="does not enable OCR"):
        HeavyPdfBackendRequest(ocr_enabled=True)
    with pytest.raises(ValueError, match="does not process large PDFs"):
        HeavyPdfBackendRequest(large_pdf_processing=True)
    with pytest.raises(ValueError, match="requires human review"):
        HeavyPdfBackendRequest(requires_human_review=False)


def test_heavy_pdf_backend_slot_markdown_documents_skip_reason() -> None:
    markdown = render_heavy_pdf_backend_slot(build_heavy_pdf_backend_slot())

    assert "# Optional Heavy PDF Backend Slot" in markdown
    assert "- Backend: `mineru`" in markdown
    assert "- Implementation present: `false`" in markdown
    assert "- OCR enabled: `false`" in markdown
    assert "Future Backend Notes" in markdown
