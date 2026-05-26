"""Shared live adapter request and response models.

These models are protocol contracts only. They do not perform network calls.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from turing_research_plus.adapters.errors import AdapterError


class AdapterTimeoutPolicy(BaseModel):
    """Timeout policy for adapter calls."""

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
    """Cache integration expected from adapters."""

    model_config = ConfigDict(extra="forbid")

    namespace: str = Field(min_length=1)
    ttl_seconds: int | None = Field(default=None, ge=1)
    cache_key_fields: list[str] = Field(default_factory=list)
    write_through: bool = True


class AdapterRequestContext(BaseModel):
    """Shared request context for live and fake adapter calls."""

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
    required_env_vars: list[str] = Field(default_factory=list)
    default_enabled: bool = False


class SourceMetadata(BaseModel):
    """Provider source metadata attached to adapter outputs."""

    model_config = ConfigDict(extra="forbid")

    provider: str = Field(min_length=1)
    source_id: str | None = None
    url: str | None = None
    retrieval_time: datetime = Field(default_factory=lambda: datetime.now(UTC))
    human_verified: bool = False
    license: str | None = None


class AdapterResultBase(BaseModel):
    """Common adapter result fields."""

    model_config = ConfigDict(extra="forbid")

    status: str = "ok"
    cache_hit: bool = False
    source_metadata: list[SourceMetadata] = Field(default_factory=list)
    error: AdapterError | None = None


class SemanticScholarPaperLookup(BaseModel):
    """Input for Semantic Scholar paper lookup."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=100)
    fields: list[str] = Field(default_factory=lambda: ["title", "authors", "year"])
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            required_env_vars=["SEMANTIC_SCHOLAR_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/paper_lookup",
                cache_key_fields=["query", "limit", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarPaperResult(AdapterResultBase):
    """Output for Semantic Scholar paper lookup."""

    papers: list[dict[str, object]] = Field(default_factory=list)
    provider: str = "semantic_scholar"


class SemanticScholarPaperIdLookup(BaseModel):
    """Input for Semantic Scholar paper lookup by provider paper id."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    fields: list[str] = Field(
        default_factory=lambda: [
            "paperId",
            "title",
            "authors",
            "year",
            "citationCount",
            "isOpenAccess",
            "abstract",
            "url",
        ]
    )
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            required_env_vars=["SEMANTIC_SCHOLAR_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/paper_id_lookup",
                cache_key_fields=["paper_id", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarPaperBatchLookup(BaseModel):
    """Input for Semantic Scholar batch paper lookup."""

    model_config = ConfigDict(extra="forbid")

    paper_ids: list[str] = Field(min_length=1, max_length=500)
    fields: list[str] = Field(
        default_factory=lambda: [
            "paperId",
            "title",
            "authors",
            "year",
            "citationCount",
            "isOpenAccess",
            "abstract",
            "url",
        ]
    )
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            required_env_vars=["SEMANTIC_SCHOLAR_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/paper_batch",
                cache_key_fields=["paper_ids", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarPaperListLookup(BaseModel):
    """Input for references or citations for one Semantic Scholar paper."""

    model_config = ConfigDict(extra="forbid")

    paper_id: str = Field(min_length=1)
    limit: int = Field(default=20, ge=1, le=100)
    fields: list[str] = Field(
        default_factory=lambda: [
            "paperId",
            "title",
            "authors",
            "year",
            "citationCount",
            "isOpenAccess",
            "url",
        ]
    )
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            required_env_vars=["SEMANTIC_SCHOLAR_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/paper_list",
                cache_key_fields=["paper_id", "limit", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarRecommendationLookup(BaseModel):
    """Input for optional Semantic Scholar recommendations."""

    model_config = ConfigDict(extra="forbid")

    paper_ids: list[str] = Field(min_length=1, max_length=100)
    limit: int = Field(default=10, ge=1, le=100)
    fields: list[str] = Field(
        default_factory=lambda: [
            "paperId",
            "title",
            "authors",
            "year",
            "citationCount",
            "isOpenAccess",
            "url",
        ]
    )
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            required_env_vars=["SEMANTIC_SCHOLAR_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/recommendations",
                cache_key_fields=["paper_ids", "limit", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarAuthorLookup(BaseModel):
    """Input for optional Semantic Scholar author lookup."""

    model_config = ConfigDict(extra="forbid")

    author_id: str = Field(min_length=1)
    fields: list[str] = Field(default_factory=lambda: ["authorId", "name", "paperCount"])
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="SEMANTIC_SCHOLAR_API_KEY",
            required_env_vars=["SEMANTIC_SCHOLAR_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="semantic_scholar/author_lookup",
                cache_key_fields=["author_id", "fields"],
            ),
            fake_adapter_name="FakeSemanticScholarAdapter",
        )
    )


class SemanticScholarAuthorResult(AdapterResultBase):
    """Output for optional Semantic Scholar author lookup."""

    authors: list[dict[str, object]] = Field(default_factory=list)
    provider: str = "semantic_scholar"


class ArxivQuery(BaseModel):
    """Input for arXiv search."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    max_results: int = Field(default=10, ge=1, le=100)
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env=None,
            required_env_vars=[],
            cache=AdapterCachePolicy(
                namespace="arxiv/search",
                cache_key_fields=["query", "max_results"],
            ),
            fake_adapter_name="FakeArxivAdapter",
        )
    )


class ArxivSearchResult(AdapterResultBase):
    """Output for arXiv search."""

    papers: list[dict[str, object]] = Field(default_factory=list)
    provider: str = "arxiv"


class WebSearchRequest(BaseModel):
    """Input for optional web search."""

    model_config = ConfigDict(extra="forbid")

    query: str = Field(min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    source_hygiene_required: bool = True
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="APIFY_TOKEN",
            required_env_vars=["APIFY_TOKEN"],
            cache=AdapterCachePolicy(
                namespace="web/search",
                cache_key_fields=["query", "limit"],
            ),
            fake_adapter_name="FakeWebSearchAdapter",
        )
    )


class WebSearchResult(AdapterResultBase):
    """Output for optional web search."""

    results: list[dict[str, object]] = Field(default_factory=list)
    provider: str = "web_search"


class WebFetchRequest(BaseModel):
    """Input for optional public web fetch."""

    model_config = ConfigDict(extra="forbid")

    url: HttpUrl
    source_hygiene_required: bool = True
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="APIFY_TOKEN",
            required_env_vars=["APIFY_TOKEN"],
            cache=AdapterCachePolicy(
                namespace="web/fetch",
                cache_key_fields=["url"],
            ),
            fake_adapter_name="FakeWebFetchAdapter",
        )
    )


class WebFetchResult(AdapterResultBase):
    """Output for optional public web fetch."""

    url: str
    markdown: str | None = None
    evidence: list[dict[str, object]] = Field(default_factory=list)
    provider: str = "web_fetch"


class LLMCompletionRequest(BaseModel):
    """Input for OpenAI-compatible LLM adapter."""

    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    model: str = Field(default="configured-by-env", min_length=1)
    max_tokens: int = Field(default=1024, ge=1)
    context: AdapterRequestContext = Field(
        default_factory=lambda: AdapterRequestContext(
            api_key_env="OPENAI_API_KEY",
            required_env_vars=["OPENAI_API_KEY"],
            cache=AdapterCachePolicy(
                namespace="openai_compatible/completion",
                cache_key_fields=["prompt", "model", "max_tokens"],
                write_through=False,
            ),
            fake_adapter_name="FakeOpenAICompatibleLLMAdapter",
        )
    )


class LLMCompletionResult(AdapterResultBase):
    """Output for OpenAI-compatible LLM adapter."""

    text: str | None = None
    model: str | None = None
    provider: str = "openai_compatible"


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
            required_env_vars=[],
            live_test_marker="manual",
            cache=AdapterCachePolicy(
                namespace="pdf/converter",
                cache_key_fields=["pdf_path", "extract_figures", "extract_tables"],
            ),
            fake_adapter_name="FakePDFConverterAdapter",
        )
    )


class PDFConversionResult(AdapterResultBase):
    """Output for replaceable local PDF converter adapter."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    markdown_path: Path | None = None
    assets: list[Path] = Field(default_factory=list)
    page_map_path: Path | None = None
    converter_used: str | None = None
