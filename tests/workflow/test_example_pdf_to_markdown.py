from __future__ import annotations

from pathlib import Path

from tests.workflow.example_helpers import assert_example_contract, read_json, to_pretty_json

from tuling_research.pdf.models import PDFMarkdownInput, PDFToolStatus
from tuling_research.pdf.pipeline import PDFMarkdownPipeline


def create_fixture_pdf(path: Path, text: str) -> None:
    import fitz

    document = fitz.open()
    page = document.new_page()
    page.insert_text((72, 72), text)
    document.save(str(path))
    document.close()


def test_pdf_to_markdown_example_dry_run_outputs_required_artifacts(tmp_path: Path) -> None:
    required = {"PDFMarkdownOutput", "markdown artifact", "quality report", "cache hit test"}
    assert_example_contract("pdf-to-markdown-demo", required)
    request = read_json("pdf-to-markdown-demo/input/request.json")
    pdf_path = tmp_path / "fixture.pdf"
    create_fixture_pdf(pdf_path, request["fixture_text"])
    pipeline = PDFMarkdownPipeline(tmp_path / "cache")

    first = pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))
    second = pipeline.to_markdown(PDFMarkdownInput(pdf_path=pdf_path, output_dir=tmp_path / "out"))
    markdown = first.markdown_path.read_text(encoding="utf-8")
    output = {
        "PDFMarkdownOutput": first.model_dump(mode="json"),
        "markdown artifact": markdown,
        "quality report": {
            "quality_score": first.quality_score,
            "warnings": first.warnings,
            "converter_used": first.converter_used,
        },
        "cache hit test": {"first": first.cache_hit, "second": second.cache_hit},
    }

    assert set(output) == required
    assert first.status == PDFToolStatus.OK
    assert first.cache_hit is False
    assert second.cache_hit is True
    assert "tiny local PDF fixture" in markdown
    assert first.quality_score > 0
    assert "PDFMarkdownOutput" in to_pretty_json(output)
