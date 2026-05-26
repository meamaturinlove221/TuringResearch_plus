"""PDF to Markdown pipeline."""

from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from turing_research.cache.keys import CacheKey, build_cache_key
from turing_research.cache.manager import CacheManager
from turing_research.pdf.converters.pymupdf_converter import (
    ConverterUnavailableError,
    PyMuPDFConverter,
)
from turing_research.pdf.extractors.sectionizer import sectionize_text
from turing_research.pdf.models import (
    PDFCacheLookupInput,
    PDFErrorCode,
    PDFMarkdownContentInput,
    PDFMarkdownContentOutput,
    PDFMarkdownError,
    PDFMarkdownInput,
    PDFMarkdownOutput,
    PDFPageMapEntry,
    PDFToolStatus,
)
from turing_research.pdf.quality import score_markdown


class PDFMarkdownPipeline:
    """Minimal local PDF to Markdown pipeline."""

    def __init__(
        self,
        cache_dir: str | Path,
        converter: PyMuPDFConverter | None = None,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache = CacheManager(self.cache_dir / "pdf" / "markdown")
        self.converter = converter or PyMuPDFConverter()

    def cache_lookup(self, request: PDFCacheLookupInput) -> PDFMarkdownOutput | None:
        """Return cached PDF Markdown output if present."""

        key = self._cache_key(request.pdf_path)
        entry = self.cache.get(key)
        if entry is None:
            return None
        output = PDFMarkdownOutput.model_validate(entry.value)
        return output.model_copy(update={"cache_hit": True})

    def markdown_content(self, request: PDFMarkdownContentInput) -> PDFMarkdownContentOutput:
        """Read cached Markdown content for a PDF."""

        output = self.cache_lookup(PDFCacheLookupInput(pdf_path=request.pdf_path))
        if output is None:
            return PDFMarkdownContentOutput(
                status=PDFToolStatus.ERROR,
                error=PDFMarkdownError(
                    code=PDFErrorCode.CACHE_MISS,
                    message="PDF Markdown output is not available in local cache",
                ),
            )
        try:
            markdown = output.markdown_path.read_text(encoding="utf-8")
        except OSError as exc:
            return PDFMarkdownContentOutput(
                status=PDFToolStatus.ERROR,
                output=output,
                error=PDFMarkdownError(
                    code=PDFErrorCode.CACHE_MISS,
                    message=f"Cached Markdown file is not readable: {exc}",
                ),
            )
        return PDFMarkdownContentOutput(status=PDFToolStatus.OK, markdown=markdown, output=output)

    def to_markdown(self, request: PDFMarkdownInput) -> PDFMarkdownOutput:
        """Convert a local PDF file to Markdown and cache the output metadata."""

        if not request.force:
            cached = self.cache_lookup(PDFCacheLookupInput(pdf_path=request.pdf_path))
            if cached is not None:
                return cached.model_copy(update={"cache_hit": True})

        pdf_path = request.pdf_path
        if not pdf_path.exists():
            return self._error_output(
                request,
                PDFErrorCode.MISSING_FILE,
                "PDF path does not exist",
            )

        output_dir = request.output_dir or (self.cache_dir / "pdf" / "markdown_files")
        output_dir.mkdir(parents=True, exist_ok=True)
        stem = self._file_stem(pdf_path)
        markdown_path = output_dir / f"{stem}.md"
        page_map_path = output_dir / f"{stem}.page_map.json"

        try:
            converted = self.converter.convert(pdf_path)
        except ConverterUnavailableError as exc:
            return self._error_output(request, PDFErrorCode.CONVERTER_UNAVAILABLE, str(exc))
        except Exception as exc:
            return self._error_output(request, PDFErrorCode.INVALID_PDF, f"Invalid PDF: {exc}")

        markdown_parts: list[str] = [f"# {converted.title.strip() or pdf_path.stem}".strip()]
        page_map: list[PDFPageMapEntry] = []
        current_line = len(markdown_parts)
        for page in converted.pages:
            page_lines = [f"<!-- page:{page.page_number} -->"]
            sectionized = sectionize_text(page.text)
            if sectionized:
                page_lines.append(sectionized)
            start_line = current_line + 1
            end_line = start_line + len(page_lines) - 1
            page_map.append(
                PDFPageMapEntry(
                    page_number=page.page_number,
                    start_line=start_line,
                    end_line=end_line,
                )
            )
            markdown_parts.extend(page_lines)
            current_line = end_line

        markdown = "\n\n".join(markdown_parts).strip() + "\n"
        warnings = list(converted.warnings)
        title_only_markdown = f"# {converted.title.strip() or pdf_path.stem}"
        if not markdown.strip() or markdown.strip() == title_only_markdown:
            warnings.append("pdf produced empty markdown content")

        markdown_path.write_text(markdown, encoding="utf-8")
        page_map_path.write_text(
            json.dumps([entry.model_dump(mode="json") for entry in page_map], indent=2),
            encoding="utf-8",
        )

        output = PDFMarkdownOutput(
            title=converted.title,
            markdown_path=markdown_path,
            markdown_chars=len(markdown),
            converter_used=converted.converter_used,
            assets=[],
            page_map_path=page_map_path,
            quality_score=score_markdown(markdown, warnings),
            warnings=warnings,
            cache_hit=False,
        )
        self.cache.put(
            self._cache_key(pdf_path),
            output.model_dump(mode="json"),
            {
                "namespace": "pdf/markdown",
                "pdf_path_sha256": self._path_digest(pdf_path),
                "markdown_path": str(markdown_path),
            },
        )
        return output

    def _error_output(
        self,
        request: PDFMarkdownInput,
        code: PDFErrorCode,
        message: str,
    ) -> PDFMarkdownOutput:
        output_dir = request.output_dir or (self.cache_dir / "pdf" / "markdown_files")
        stem = self._file_stem(request.pdf_path)
        return PDFMarkdownOutput(
            status=PDFToolStatus.ERROR,
            title=request.pdf_path.stem or "Untitled PDF",
            markdown_path=output_dir / f"{stem}.md",
            markdown_chars=0,
            converter_used="none",
            assets=[],
            page_map_path=output_dir / f"{stem}.page_map.json",
            quality_score=0.0,
            warnings=[],
            cache_hit=False,
            error=PDFMarkdownError(code=code, message=message),
        )

    def _cache_key(self, pdf_path: Path) -> CacheKey:
        return build_cache_key("pdf/markdown", str(pdf_path.resolve()))

    def _file_stem(self, pdf_path: Path) -> str:
        return self._path_digest(pdf_path)[:16]

    def _path_digest(self, pdf_path: Path) -> str:
        return sha256(str(pdf_path.resolve()).encode("utf-8")).hexdigest()
