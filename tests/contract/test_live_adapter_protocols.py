from __future__ import annotations

import inspect
import tomllib
from pathlib import Path

from tuling_research_plus.adapters.protocols import (
    AdapterCachePolicy,
    AdapterError,
    AdapterErrorCode,
    AdapterRequestContext,
    AdapterRetryPolicy,
    AdapterTimeoutPolicy,
    ApifyWebAdapter,
    ArxivAdapter,
    ArxivQuery,
    LLMCompletionRequest,
    OpenAICompatibleLLMAdapter,
    PDFConversionRequest,
    PDFConverterAdapter,
    RateLimitPolicy,
    SemanticScholarAdapter,
    SemanticScholarPaperLookup,
    WebFetchRequest,
)

ROOT = Path(__file__).resolve().parents[2]


def test_live_adapter_contract_exists_and_is_protocol_only() -> None:
    content = (ROOT / "contracts" / "live_adapters.yaml").read_text(encoding="utf-8")

    for adapter_name in (
        "SemanticScholarAdapter",
        "ArxivAdapter",
        "ApifyWebAdapter",
        "OpenAICompatibleLLMAdapter",
        "PDFConverterAdapter",
    ):
        assert adapter_name in content

    assert "implementation_status: protocol_only" in content
    assert "fake_adapter_equivalent" in content
    assert "live_test_marker" in content


def test_shared_adapter_policies_validate_defaults() -> None:
    timeout = AdapterTimeoutPolicy()
    retry = AdapterRetryPolicy()
    rate_limit = RateLimitPolicy()
    cache = AdapterCachePolicy(namespace="test/adapter", cache_key_fields=["query"])
    context = AdapterRequestContext(cache=cache, fake_adapter_name="FakeAdapter")

    assert timeout.connect_seconds > 0
    assert retry.max_attempts >= 1
    assert "timeout" in retry.retry_on
    assert rate_limit.on_limit == "return_typed_error"
    assert context.dry_run is True
    assert context.live_enabled is False
    assert context.live_test_marker == "live"


def test_adapter_error_codes_are_stable() -> None:
    error = AdapterError(
        code=AdapterErrorCode.MISSING_API_KEY,
        message="missing test key",
        retryable=False,
        provider="semantic_scholar",
    )

    assert error.code == "missing_api_key"
    assert error.retryable is False
    assert AdapterErrorCode.RATE_LIMITED == "rate_limited"


def test_semantic_scholar_request_declares_live_policy_and_fake_adapter() -> None:
    request = SemanticScholarPaperLookup(query="test")

    assert request.context.api_key_env == "SEMANTIC_SCHOLAR_API_KEY"
    assert request.context.cache.namespace == "semantic_scholar/paper_lookup"
    assert request.context.fake_adapter_name == "FakeSemanticScholarAdapter"
    assert request.context.live_enabled is False


def test_arxiv_request_declares_live_policy_and_fake_adapter() -> None:
    request = ArxivQuery(query="test")

    assert request.context.api_key_env == "ARXIV_API_KEY"
    assert request.context.cache.namespace == "arxiv/search"
    assert request.context.fake_adapter_name == "FakeArxivAdapter"


def test_apify_request_declares_source_hygiene_and_fake_adapter() -> None:
    request = WebFetchRequest(url="https://example.com")

    assert request.source_hygiene_required is True
    assert request.context.api_key_env == "APIFY_TOKEN"
    assert request.context.fake_adapter_name == "FakeApifyWebAdapter"


def test_openai_compatible_request_is_optional_and_fakeable() -> None:
    request = LLMCompletionRequest(prompt="Summarize evidence.")

    assert request.context.api_key_env == "OPENAI_API_KEY"
    assert request.context.cache.write_through is False
    assert request.context.fake_adapter_name == "FakeOpenAICompatibleLLMAdapter"


def test_pdf_converter_request_has_no_live_api_key_requirement() -> None:
    request = PDFConversionRequest(pdf_path=Path("paper.pdf"))

    assert request.context.api_key_env is None
    assert request.context.cache.namespace == "pdf/converter"
    assert request.context.fake_adapter_name == "FakePDFConverterAdapter"


def test_protocol_methods_are_declared_without_implementing_network_clients() -> None:
    protocols = [
        (SemanticScholarAdapter, "paper_lookup"),
        (ArxivAdapter, "search"),
        (ApifyWebAdapter, "fetch"),
        (OpenAICompatibleLLMAdapter, "complete"),
        (PDFConverterAdapter, "convert"),
    ]

    for protocol, method_name in protocols:
        assert getattr(protocol, "_is_protocol", False) is True
        method = getattr(protocol, method_name)
        assert inspect.isfunction(method)


def test_live_policy_docs_state_default_skip_and_no_key_failure() -> None:
    policy = (ROOT / "docs" / "live-test-policy.md").read_text(encoding="utf-8").lower()

    assert "default tests must pass without" in policy
    assert "missing keys must skip live tests or return typed missing-key errors" in policy
    assert "ci must not run live tests by default" in policy


def test_pytest_default_skips_live_and_manual_markers() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    addopts = pyproject["tool"]["pytest"]["ini_options"]["addopts"]

    assert "not live" in addopts
    assert "not manual" in addopts
