"""Pydantic models for the PDF to Markdown service boundary."""

from enum import StrEnum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PdfRoute(StrEnum):
    """Supported Phase 1 PDF conversion routes."""

    PYMUPDF_LOCAL = "pymupdf_local"


class PDFToolStatus(StrEnum):
    """PDF tool result status."""

    OK = "ok"
    ERROR = "error"


class PDFErrorCode(StrEnum):
    """Typed PDF error codes."""

    INVALID_PDF = "invalid_pdf"
    MISSING_FILE = "missing_file"
    CACHE_MISS = "cache_miss"
    CONVERTER_UNAVAILABLE = "converter_unavailable"


class PDFMarkdownError(BaseModel):
    """Typed PDF Markdown error."""

    model_config = ConfigDict(extra="forbid")

    code: PDFErrorCode
    message: str = Field(min_length=1)


class PdfSource(BaseModel):
    """Addressable PDF input."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    uri: str = Field(min_length=1)
    sha256: str | None = None


class PdfMarkdownOptions(BaseModel):
    """Options for the minimal PDF Markdown boundary."""

    model_config = ConfigDict(extra="forbid")

    route: PdfRoute = PdfRoute.PYMUPDF_LOCAL
    include_page_markers: bool = True
    extract_images: bool = False
    max_pages: int | None = Field(default=None, gt=0)


class PdfMarkdownRequest(BaseModel):
    """Request accepted by the PDF Markdown service protocol."""

    model_config = ConfigDict(extra="forbid")

    source: PdfSource
    options: PdfMarkdownOptions = Field(default_factory=PdfMarkdownOptions)
    dry_run: bool = True


class MarkdownPage(BaseModel):
    """Markdown extracted from one PDF page."""

    model_config = ConfigDict(extra="forbid")

    page_number: int = Field(ge=1)
    markdown: str
    evidence_locator: str = Field(min_length=1)


class PdfMarkdownResult(BaseModel):
    """PDF Markdown conversion result."""

    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    pages: list[MarkdownPage] = Field(default_factory=list)
    route: PdfRoute = PdfRoute.PYMUPDF_LOCAL
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PDFInspectInput(BaseModel):
    """Input for pdf.inspect."""

    model_config = ConfigDict(extra="forbid")

    pdf_path: Path


class PDFInspectOutput(BaseModel):
    """Output for pdf.inspect."""

    model_config = ConfigDict(extra="forbid")

    status: PDFToolStatus
    pdf_path: Path
    exists: bool
    title: str | None = None
    page_count: int | None = Field(default=None, ge=0)
    warnings: list[str] = Field(default_factory=list)
    error: PDFMarkdownError | None = None


class PDFMarkdownInput(BaseModel):
    """Input for pdf.to_markdown."""

    model_config = ConfigDict(extra="forbid")

    pdf_path: Path
    output_dir: Path | None = None
    force: bool = False


class PDFCacheLookupInput(BaseModel):
    """Input for pdf.cache_lookup."""

    model_config = ConfigDict(extra="forbid")

    pdf_path: Path


class PDFMarkdownContentInput(BaseModel):
    """Input for pdf.markdown_content."""

    model_config = ConfigDict(extra="forbid")

    pdf_path: Path


class PDFPageMapEntry(BaseModel):
    """Map from PDF page to markdown line range."""

    model_config = ConfigDict(extra="forbid")

    page_number: int = Field(ge=1)
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)


class PDFMarkdownOutput(BaseModel):
    """Output for pdf.to_markdown and cache-backed markdown lookup."""

    model_config = ConfigDict(extra="forbid")

    status: PDFToolStatus = PDFToolStatus.OK
    title: str
    markdown_path: Path
    markdown_chars: int = Field(ge=0)
    converter_used: str
    assets: list[Path] = Field(default_factory=list)
    page_map_path: Path
    quality_score: float = Field(ge=0.0, le=1.0)
    warnings: list[str] = Field(default_factory=list)
    cache_hit: bool
    error: PDFMarkdownError | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            return "Untitled PDF"
        return value


class PDFMarkdownContentOutput(BaseModel):
    """Output for pdf.markdown_content."""

    model_config = ConfigDict(extra="forbid")

    status: PDFToolStatus
    markdown: str | None = None
    output: PDFMarkdownOutput | None = None
    error: PDFMarkdownError | None = None
