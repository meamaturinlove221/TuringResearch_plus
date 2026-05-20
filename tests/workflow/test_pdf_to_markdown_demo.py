from pathlib import Path

from tuling_research.pdf.models import PDFMarkdownOutput


def test_pdf_to_markdown_demo_uses_fixture_style_output(tmp_path: Path) -> None:
    markdown_path = tmp_path / "fixture.md"
    markdown_path.write_text("# Fixture PDF\n\nConverted text.", encoding="utf-8")
    output = PDFMarkdownOutput(
        title="Fixture PDF",
        markdown_path=markdown_path,
        markdown_chars=len(markdown_path.read_text(encoding="utf-8")),
        converter_used="fixture",
        assets=[],
        page_map_path=tmp_path / "page_map.json",
        quality_score=1.0,
        warnings=[],
        cache_hit=False,
    )

    assert output.markdown_path.exists()
    assert output.title == "Fixture PDF"
