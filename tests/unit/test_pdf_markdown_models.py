import pytest
from pydantic import ValidationError

from turing_research.pdf.models import (
    MarkdownPage,
    PdfMarkdownOptions,
    PdfMarkdownRequest,
    PdfRoute,
    PdfSource,
)


def test_pdf_markdown_request_defaults_to_dry_run_and_pymupdf_route() -> None:
    request = PdfMarkdownRequest(
        source=PdfSource(source_id="pdf-1", uri="file:///tmp/example.pdf"),
    )

    assert request.dry_run is True
    assert request.options.route == PdfRoute.PYMUPDF_LOCAL


def test_pdf_markdown_rejects_page_zero() -> None:
    with pytest.raises(ValidationError):
        MarkdownPage(page_number=0, markdown="", evidence_locator="p.0")


def test_pdf_markdown_options_reject_non_positive_max_pages() -> None:
    with pytest.raises(ValidationError):
        PdfMarkdownOptions(max_pages=0)
