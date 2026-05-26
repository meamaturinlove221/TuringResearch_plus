from __future__ import annotations

from datetime import datetime

from turing_research_plus.adapters.errors import AdapterError, AdapterErrorCode
from turing_research_plus.adapters.models import (
    AdapterCachePolicy,
    AdapterRequestContext,
    ArxivQuery,
    LLMCompletionRequest,
    PDFConversionRequest,
    SemanticScholarPaperLookup,
    SourceMetadata,
    WebFetchRequest,
    WebSearchRequest,
)


def test_request_context_defaults_keep_live_disabled() -> None:
    context = AdapterRequestContext(
        cache=AdapterCachePolicy(namespace="test/cache"),
        fake_adapter_name="FakeAdapter",
    )

    assert context.dry_run is True
    assert context.live_enabled is False
    assert context.default_enabled is False
    assert context.live_test_marker == "live"


def test_source_metadata_is_not_human_verified_by_default() -> None:
    metadata = SourceMetadata(provider="semantic_scholar", source_id="S2-1")

    assert metadata.human_verified is False
    assert isinstance(metadata.retrieval_time, datetime)


def test_adapter_error_codes_include_live_disabled() -> None:
    error = AdapterError(
        code=AdapterErrorCode.LIVE_DISABLED,
        message="live adapter disabled",
        retryable=False,
    )

    assert error.code == "live_disabled"


def test_adapter_requests_declare_required_env_and_fake_equivalent() -> None:
    semantic = SemanticScholarPaperLookup(query="VGGT")
    arxiv = ArxivQuery(query="VGGT")
    web_search = WebSearchRequest(query="VGGT")
    web_fetch = WebFetchRequest(url="https://example.com")
    llm = LLMCompletionRequest(prompt="Summarize evidence.")
    pdf = PDFConversionRequest(pdf_path="paper.pdf")

    assert semantic.context.required_env_vars == ["SEMANTIC_SCHOLAR_API_KEY"]
    assert semantic.context.fake_adapter_name == "FakeSemanticScholarAdapter"
    assert arxiv.context.required_env_vars == []
    assert arxiv.context.fake_adapter_name == "FakeArxivAdapter"
    assert web_search.context.required_env_vars == ["APIFY_TOKEN"]
    assert web_search.context.fake_adapter_name == "FakeWebSearchAdapter"
    assert web_fetch.context.required_env_vars == ["APIFY_TOKEN"]
    assert web_fetch.context.fake_adapter_name == "FakeWebFetchAdapter"
    assert llm.context.required_env_vars == ["OPENAI_API_KEY"]
    assert llm.context.fake_adapter_name == "FakeOpenAICompatibleLLMAdapter"
    assert pdf.context.required_env_vars == []
    assert pdf.context.fake_adapter_name == "FakePDFConverterAdapter"
