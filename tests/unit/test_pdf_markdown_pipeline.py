from pathlib import Path

from turing_research.pdf.models import PDFErrorCode, PDFMarkdownInput, PDFToolStatus
from turing_research.pdf.pipeline import PDFMarkdownPipeline
from turing_research.pdf.tools import pdf_markdown_content
from turing_research.settings import CoreSettings


def create_pdf(path: Path, text: str | None = None) -> None:
    import fitz

    document = fitz.open()
    page = document.new_page()
    if text is not None:
        page.insert_text((72, 72), text)
    document.save(str(path))
    document.close()


def test_local_fixture_pdf_converts_to_markdown(tmp_path) -> None:
    pdf_path = tmp_path / "fixture.pdf"
    create_pdf(pdf_path, "Introduction\nThis is a cached PDF fixture.")
    pipeline = PDFMarkdownPipeline(tmp_path / "cache")

    output = pipeline.to_markdown(
        PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out")
    )

    assert output.status == PDFToolStatus.OK
    assert output.title == "fixture"
    assert output.markdown_path.exists()
    assert output.page_map_path.exists()
    assert output.markdown_chars > 0
    assert output.converter_used == "pymupdf"
    assert output.assets == []
    assert output.quality_score > 0
    assert output.cache_hit is False
    markdown = output.markdown_path.read_text(encoding="utf-8")
    assert "## Introduction" in markdown
    assert "cached PDF fixture" in markdown


def test_pdf_cache_hit_avoids_repeated_conversion(tmp_path) -> None:
    pdf_path = tmp_path / "fixture.pdf"
    create_pdf(pdf_path, "Results\nFirst conversion.")
    pipeline = PDFMarkdownPipeline(tmp_path / "cache")

    first = pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))
    first.markdown_path.write_text("cached marker", encoding="utf-8")
    second = pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))

    assert first.cache_hit is False
    assert second.cache_hit is True
    assert second.markdown_path.read_text(encoding="utf-8") == "cached marker"


def test_invalid_pdf_returns_typed_error(tmp_path) -> None:
    pdf_path = tmp_path / "invalid.pdf"
    pdf_path.write_text("not a pdf", encoding="utf-8")
    pipeline = PDFMarkdownPipeline(tmp_path / "cache")

    output = pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))

    assert output.status == PDFToolStatus.ERROR
    assert output.error is not None
    assert output.error.code == PDFErrorCode.INVALID_PDF
    assert output.markdown_chars == 0


def test_empty_pdf_gives_warning(tmp_path) -> None:
    pdf_path = tmp_path / "empty.pdf"
    create_pdf(pdf_path, None)
    pipeline = PDFMarkdownPipeline(tmp_path / "cache")

    output = pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))

    assert output.status == PDFToolStatus.OK
    assert any("no extractable text" in warning for warning in output.warnings)
    assert output.quality_score < 1.0


def test_markdown_content_reads_cached_result(tmp_path) -> None:
    pdf_path = tmp_path / "fixture.pdf"
    create_pdf(pdf_path, "Discussion\nCached content.")
    settings = CoreSettings(cache_dir=tmp_path / "cache")
    pipeline = PDFMarkdownPipeline(settings.cache_dir)
    pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))

    result = pdf_markdown_content(pdf_path, settings=settings)

    assert result["status"] == PDFToolStatus.OK
    assert "Cached content." in result["markdown"]
    assert result["output"]["cache_hit"] is True
