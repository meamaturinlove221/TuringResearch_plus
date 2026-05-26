from __future__ import annotations

from pathlib import Path

from turing_research_plus.adapters.fake import (
    FakeArxivAdapter,
    FakeOpenAICompatibleLLMAdapter,
    FakePDFConverterAdapter,
    FakeSemanticScholarAdapter,
    FakeWebFetchAdapter,
    FakeWebSearchAdapter,
)
from turing_research_plus.adapters.models import (
    ArxivQuery,
    LLMCompletionRequest,
    PDFConversionRequest,
    SemanticScholarPaperLookup,
    WebFetchRequest,
    WebSearchRequest,
)


def test_fake_semantic_scholar_result_has_source_metadata() -> None:
    result = FakeSemanticScholarAdapter().paper_lookup(
        SemanticScholarPaperLookup(query="VGGT", limit=1)
    )

    assert result.papers[0]["title"] == "Fake result for VGGT"
    assert result.source_metadata[0].provider == "semantic_scholar"
    assert result.source_metadata[0].human_verified is False


def test_fake_arxiv_result_is_deterministic() -> None:
    result = FakeArxivAdapter().search(ArxivQuery(query="sparse conv"))

    assert result.papers[0]["arxiv_id"] == "0000.00000"
    assert result.source_metadata[0].human_verified is False


def test_fake_web_search_and_fetch_do_not_need_network() -> None:
    search = FakeWebSearchAdapter().search(WebSearchRequest(query="VGGT"))
    fetch = FakeWebFetchAdapter().fetch(WebFetchRequest(url="https://example.com/page"))

    assert search.results[0]["url"] == "https://example.com/fake-search-result"
    assert "# Fake fetch" in (fetch.markdown or "")
    assert fetch.source_metadata[0].human_verified is False


def test_fake_llm_completion_is_not_human_verified() -> None:
    result = FakeOpenAICompatibleLLMAdapter().complete(
        LLMCompletionRequest(prompt="Summarize evidence.")
    )

    assert result.text == "Fake completion for: Summarize evidence."
    assert result.source_metadata[0].human_verified is False


def test_fake_pdf_converter_returns_paths_without_touching_files(tmp_path: Path) -> None:
    result = FakePDFConverterAdapter().convert(
        PDFConversionRequest(pdf_path=Path("paper.pdf"), output_dir=tmp_path)
    )

    assert result.markdown_path == tmp_path / "paper.md"
    assert result.page_map_path == tmp_path / "paper.page_map.json"
    assert result.converter_used == "fake_pdf_converter"
