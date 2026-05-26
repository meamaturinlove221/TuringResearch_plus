"""Local PDF inspection."""

from __future__ import annotations

from pathlib import Path

from turing_research.pdf.models import (
    PDFErrorCode,
    PDFInspectOutput,
    PDFMarkdownError,
    PDFToolStatus,
)


def inspect_pdf(pdf_path: str | Path) -> PDFInspectOutput:
    """Inspect a local PDF path without calling external APIs."""

    path = Path(pdf_path)
    if not path.exists():
        return PDFInspectOutput(
            status=PDFToolStatus.ERROR,
            pdf_path=path,
            exists=False,
            error=PDFMarkdownError(
                code=PDFErrorCode.MISSING_FILE,
                message="PDF path does not exist",
            ),
        )

    try:
        import fitz  # type: ignore[import-untyped]

        with fitz.open(str(path)) as document:
            title = str(document.metadata.get("title") or "").strip() or path.stem
            page_count = int(document.page_count)
    except ModuleNotFoundError:
        return PDFInspectOutput(
            status=PDFToolStatus.ERROR,
            pdf_path=path,
            exists=True,
            error=PDFMarkdownError(
                code=PDFErrorCode.CONVERTER_UNAVAILABLE,
                message="PyMuPDF is required for PDF inspection",
            ),
        )
    except Exception as exc:
        return PDFInspectOutput(
            status=PDFToolStatus.ERROR,
            pdf_path=path,
            exists=True,
            error=PDFMarkdownError(
                code=PDFErrorCode.INVALID_PDF,
                message=f"Invalid PDF: {exc}",
            ),
        )

    warnings = []
    if page_count == 0:
        warnings.append("pdf contains no pages")
    return PDFInspectOutput(
        status=PDFToolStatus.OK,
        pdf_path=path,
        exists=True,
        title=title,
        page_count=page_count,
        warnings=warnings,
    )
