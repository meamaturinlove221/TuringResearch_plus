"""Live adapter protocol models for TulingResearch Plus v0.2.0 planning.

These are interface contracts only. They do not perform live network calls.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class AdapterErrorCode(str):
    """Stable adapter error code constants."""

    MISSING_API_KEY = "missing_api_key"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    RETRY_EXHAUSTED = "retry_exhausted"
    PROVIDER_ERROR = "provider_error"
    INVALID_RESPONSE = "invalid_response"
    UNSUPPORTED = "unsupported"
    SOURCE_HYGIENE_BLOCKED = "source_hygiene_blocked"


class AdapterError(BaseModel):
    """Typed error returned by adapter boundaries."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    retryable: bool = False
    provider: str | None = None
    status_code: int | None = Field(default=None, ge=100, le=599)
    details: dict[str, str] = Field(default_factory=dict)


class AdapterTimeoutPolicy(BaseModel):
    """Timeout policy for live adapter calls."""

    model_config = ConfigDict(extra="forbid")

    connect_seconds: float = Field(default=5.0, gt=0)
    read_seconds: float = Field(default=30.0, gt=0)
    total_seconds: float = Field(default=60.0, gt=0)


class AdapterRetryPolicy(BaseModel):
    """Retry policy for transient adapter failures."""

    model_config = ConfigDict(extra="forbid")

    max_attempts: int = Field(default=3, ge=1)
    backoff_seconds: float = Field(default=1.0, ge=0)
    retry_on: list[str] = Field(default_factory=lambda: ["timeout", "rate_limited"])


class RateLimitPolicy(BaseModel):
    """Rate limit policy recorded by adapter configuration."""

    model_config = ConfigDict(extra="forbid")

    requests_per_minute: int | None = Field(default=None, ge=1)
    provider_quota_label: str | None = None
    on_limit: str = "return_typed_error"


class AdapterCachePolicy(BaseModel):
    """Cache integration expected from live adapters."""

    model_config = ConfigDict(extra="forbid")

    namespace: str = Field(min_length=1)
    ttl_seconds: int | None = Field(default=None, ge=1)
    cache_key_fields: list[str] = Field(default_factory=list)
    write_through: bool = True


class AdapterRequestContext(BaseModel):
    """Shared request context for live adapter calls."""

    model_config = ConfigDict(extra="forbid")

    dry_run: bool = True
    live_enabled: bool = False
    api_key_env: str | None = None
    timeout: AdapterTimeoutPolicy = Field(default_factory=AdapterTimeoutPolicy)
    retry: AdapterRetryPolicy = Field(default_factory=AdapterRetryPolicy)
    rate_limit: RateLimitPolicy = Field(default_factory=RateLimitPolicy)
    cache: AdapterCachePolicy
    live_test_marker: str = "live"
    fake_adapter_name: str = Field(min_length=1)


class SemanticScholarPaperLookup(BaseModel):
    """Input for Semantic Scholar paper lookup."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
    fields: list[str] = Field(default_factory=lambda: ["title", "authors", "year"])
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/paper_lookup",
                cache_key_fields=["query", "limit", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarPaperResult(BaseModel):
    """Output for Semantic Scholar paper lookup."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"
    papers: list[dict[str, object]] = Field(default_factory=list)
    cache_hit: bool = False
    provider: str = "semantic_scholar"
    error: AdapterError | None = None


class ArxivQuery(BaseModel):
    """Input for arXiv search."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    max_results: int = Field(default=10, ge=1, le=100)
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="ARXIV_API_KEY",
            cache=AdapterCachePolicy(
                namespace="arxiv/search",
                cache_key_fields=["query", "max_results"],
            ),
            fake_adapter_name="FakeArxivAdapter",
        )
    )


class ArxivSearchResult(BaseModel):
    """Output for arXiv search."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"
    papers: list[dict[str, object]] = Field(default_factory=list)
    cache_hit: bool = False
    provider: str = "arxiv"
    error: AdapterError | None = None


class WebFetchRequest(BaseModel):
    """Input for optional Apify web fetch."""

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    source_hygiene_required: bool = True
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="APIFY_TOKEN",
            cache=AdapterCachePolicy(
                namespace="apify/web_fetch",
                cache_key_fields=["url"],
            ),
            fake_adapter_name="FakeApifyWebAdapter",
        )
    )


class WebFetchResult(BaseModel):
    """Output for optional Apify web fetch."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"
    url: str
    markdown: str | None = None
    evidence: list[dict[str, object]] = Field(default_factory=list)
    cache_hit: bool = False
    provider: str = "apify"
    error: AdapterError | None = None


class LLMCompletionRequest(BaseModel):
    """Input for OpenAI-compatible LLM adapter."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    model: str = Field(default="configured-by-env", min_length=1)
    max_tokens: int = Field(default=1024, ge=1)
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="OPENAI_API_KEY",
            cache=AdapterCachePolicy(
                namespace="openai_compatible/completion",
                cache_key_fields=["prompt", "model", "max_tokens"],
                write_through=False,
            ),
            fake_adapter_name="FakeOpenAICompatibleLLMAdapter",
        )
    )


class LLMCompletionResult(BaseModel):
    """Output for OpenAI-compatible LLM adapter."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"
    text: str | None = None
    model: str | None = None
    provider: str = "openai_compatible"
    error: AdapterError | None = None


class PDFConversionRequest(BaseModel):
    """Input for replaceable PDF converter adapter."""

    model_config = ConfigDict(extra="forbid")

    pdf_path: Path
    output_dir: Path | None = None
    extract_figures: bool = False
    extract_tables: bool = False
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env=None,
            cache=AdapterCachePolicy(
                namespace="pdf/converter",
                cache_key_fields=["pdf_path", "extract_figures", "extract_tables"],
            ),
            fake_adapter_name="FakePDFConverterAdapter",
        )
    )


class PDFConversionResult(BaseModel):
    """Output for replaceable PDF converter adapter."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    status: str = "ok"
    markdown_path: Path | None = None
    assets: list[Path] = Field(default_factory=list)
    page_map_path: Path | None = None
    cache_hit: bool = False
    converter_used: str | None = None
    error: AdapterError | None = None


@runtime_checkable
class SemanticScholarAdapter(Protocol):
    """Protocol for optional Semantic Scholar live or fake adapters."""

    def paper_lookup(self, request: SemanticScholarPaperLookup) -> SemanticScholarPaperResult:
        """Look up papers through a live or fake Semantic Scholar adapter."""


@runtime_checkable
class ArxivAdapter(Protocol):
    """Protocol for optional arXiv live or fake adapters."""

    def search(self, request: ArxivQuery) -> ArxivSearchResult:
        """Search arXiv through a live or fake adapter."""


@runtime_checkable
class ApifyWebAdapter(Protocol):
    """Protocol for optional Apify web live or fake adapters."""

    def fetch(self, request: WebFetchRequest) -> WebFetchResult:
        """Fetch public web content through a live or fake adapter."""


@runtime_checkable
class OpenAICompatibleLLMAdapter(Protocol):
    """Protocol for optional OpenAI-compatible LLM live or fake adapters."""

    def complete(self, request: LLMCompletionRequest) -> LLMCompletionResult:
        """Run a completion through a live or fake LLM adapter."""


@runtime_checkable
class PDFConverterAdapter(Protocol):
    """Protocol for replaceable local PDF converter adapters."""

    def convert(self, request: PDFConversionRequest) -> PDFConversionResult:
        """Convert PDF input through a local or fake converter adapter."""
