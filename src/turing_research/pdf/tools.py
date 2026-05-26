"""Thin pdf.* tool wrappers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from turing_research.pdf.models import (
    PDFCacheLookupInput,
    PDFInspectInput,
    PDFMarkdownContentInput,
    PDFMarkdownInput,
)
from turing_research.pdf.service import PDFService
from turing_research.settings import CoreSettings, get_settings


def _service(settings: CoreSettings | None = None) -> PDFService:
    active_settings = settings or get_settings()
    return PDFService(active_settings.cache_dir)


def pdf_inspect(pdf_path: str | Path, settings: CoreSettings | None = None) -> dict[str, Any]:
    """Tool wrapper for pdf.inspect."""

    result = _service(settings).inspect(PDFInspectInput(pdf_path=Path(pdf_path)))
    return result.model_dump(mode="json")


def pdf_to_markdown(
    pdf_path: str | Path,
    output_dir: str | Path | None = None,
    force: bool = False,
    settings: CoreSettings | None = None,
) -> dict[str, Any]:
    """Tool wrapper for pdf.to_markdown."""

    result = _service(settings).to_markdown(
        PDFMarkdownInput(
            pdf_path=Path(pdf_path),
            output_dir=Path(output_dir) if output_dir is not None else None,
            force=force,
        )
    )
    return result.model_dump(mode="json")


def pdf_cache_lookup(
    pdf_path: str | Path,
    settings: CoreSettings | None = None,
) -> dict[str, Any] | None:
    """Tool wrapper for pdf.cache_lookup."""

    result = _service(settings).cache_lookup(PDFCacheLookupInput(pdf_path=Path(pdf_path)))
    if result is None:
        return None
    return result.model_dump(mode="json")


def pdf_markdown_content(
    pdf_path: str | Path,
    settings: CoreSettings | None = None,
) -> dict[str, Any]:
    """Tool wrapper for pdf.markdown_content."""

    result = _service(settings).markdown_content(
        PDFMarkdownContentInput(pdf_path=Path(pdf_path))
    )
    return result.model_dump(mode="json")
