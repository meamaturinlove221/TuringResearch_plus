"""Minimal PyMuPDF converter adapter."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class PDFPageText(BaseModel):
    """Extracted text for a PDF page."""

    model_config = ConfigDict(extra="forbid")

    page_number: int = Field(ge=1)
    text: str


class ConvertedPDF(BaseModel):
    """Raw converter output."""

    model_config = ConfigDict(extra="forbid")

    title: str
    pages: list[PDFPageText]
    converter_used: str = "pymupdf"
    warnings: list[str] = Field(default_factory=list)


class ConverterUnavailableError(RuntimeError):
    """Raised when the configured local converter is unavailable."""


class PyMuPDFConverter:
    """Local PyMuPDF converter adapter."""

    converter_name = "pymupdf"

    def convert(self, pdf_path: Path) -> ConvertedPDF:
        """Extract page text from a local PDF path."""

        try:
            import fitz  # type: ignore[import-untyped]
        except ModuleNotFoundError as exc:
            msg = "PyMuPDF is required for the local PDF converter"
            raise ConverterUnavailableError(msg) from exc

        pages: list[PDFPageText] = []
        warnings: list[str] = []
        with fitz.open(str(pdf_path)) as document:
            title = str(document.metadata.get("title") or "").strip() or pdf_path.stem
            for index, page in enumerate(document, start=1):
                text = page.get_text("text")
                if not text.strip():
                    warnings.append(f"page {index} contains no extractable text")
                pages.append(PDFPageText(page_number=index, text=text))

        if not pages:
            warnings.append("pdf contains no pages")

        return ConvertedPDF(title=title, pages=pages, warnings=warnings)
