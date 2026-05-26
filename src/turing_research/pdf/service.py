"""PDF service facade."""

from __future__ import annotations

from pathlib import Path

from turing_research.pdf.inspector import inspect_pdf
from turing_research.pdf.models import (
    PDFCacheLookupInput,
    PDFInspectInput,
    PDFInspectOutput,
    PDFMarkdownContentInput,
    PDFMarkdownContentOutput,
    PDFMarkdownInput,
    PDFMarkdownOutput,
)
from turing_research.pdf.pipeline import PDFMarkdownPipeline


class PDFService:
    """Service facade for pdf.* tools."""

    def __init__(self, cache_dir: str | Path) -> None:
        self.pipeline = PDFMarkdownPipeline(cache_dir)

    def inspect(self, request: PDFInspectInput) -> PDFInspectOutput:
        return inspect_pdf(request.pdf_path)

    def to_markdown(self, request: PDFMarkdownInput) -> PDFMarkdownOutput:
        return self.pipeline.to_markdown(request)

    def cache_lookup(self, request: PDFCacheLookupInput) -> PDFMarkdownOutput | None:
        return self.pipeline.cache_lookup(request)

    def markdown_content(
        self,
        request: PDFMarkdownContentInput,
    ) -> PDFMarkdownContentOutput:
        return self.pipeline.markdown_content(request)
