"""Optional Semantic Scholar live adapter.

The adapter is disabled by default and performs no network calls unless a
request explicitly sets ``context.live_enabled`` and ``context.dry_run`` is
false. Live results are retrieval metadata only; they are not human-verified.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import UTC, datetime
from importlib.util import find_spec
from typing import Any

from turing_research_plus.adapters.cache import InMemoryAdapterCache, build_adapter_cache_key
from turing_research_plus.adapters.errors import AdapterError, AdapterErrorCode
from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import (
    AdapterRequestContext,
    SemanticScholarAuthorLookup,
    SemanticScholarAuthorResult,
    SemanticScholarPaperBatchLookup,
    SemanticScholarPaperIdLookup,
    SemanticScholarPaperListLookup,
    SemanticScholarPaperLookup,
    SemanticScholarPaperResult,
    SemanticScholarRecommendationLookup,
    SourceMetadata,
)
from turing_research_plus.adapters.rate_limit import RateLimitChecker

PROVIDER = "semantic_scholar"
DEFAULT_BASE_URL = "https://api.semanticscholar.org/graph/v1"


class SemanticScholarLiveAdapter:
    """Semantic Scholar live client with fake/dry-run and typed failure paths."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        api_key_env: str = "SEMANTIC_SCHOLAR_API_KEY",
        client_factory: Callable[..., Any] | None = None,
        cache: InMemoryAdapterCache | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.client_factory = client_factory
        self.cache = cache or InMemoryAdapterCache()
        self.fake = FakeSemanticScholarAdapter()

    def paper_lookup(self, request: SemanticScholarPaperLookup) -> SemanticScholarPaperResult:
        if request.context.dry_run:
            return self.fake.paper_lookup(request)
        identity = request.query
        cached = self._cached_result(request.context, identity, request.model_dump(mode="json"))
        if cached is not None:
            return self._paper_result(cached, cache_hit=True)
        return self._get_papers(
            request.context,
            "/paper/search",
            params={
                "query": request.query,
                "limit": request.limit,
                "fields": ",".join(request.fields),
            },
            payload_path=("data",),
            cache_identity=identity,
            cache_values=request.model_dump(mode="json"),
        )

    def paper_lookup_by_id(
        self, request: SemanticScholarPaperIdLookup
    ) -> SemanticScholarPaperResult:
        if request.context.dry_run:
            return self.fake.paper_lookup_by_id(request)
        cached = self._cached_result(
            request.context, request.paper_id, request.model_dump(mode="json")
        )
        if cached is not None:
            return self._paper_result(cached, cache_hit=True)
        return self._get_papers(
            request.context,
            f"/paper/{request.paper_id}",
            params={"fields": ",".join(request.fields)},
            payload_path=None,
            cache_identity=request.paper_id,
            cache_values=request.model_dump(mode="json"),
            single=True,
        )

    def paper_batch(self, request: SemanticScholarPaperBatchLookup) -> SemanticScholarPaperResult:
        if request.context.dry_run:
            return self.fake.paper_batch(request)
        identity = ",".join(request.paper_ids)
        cached = self._cached_result(request.context, identity, request.model_dump(mode="json"))
        if cached is not None:
            return self._paper_result(cached, cache_hit=True)
        return self._post_papers(
            request.context,
            "/paper/batch",
            params={"fields": ",".join(request.fields)},
            json_body={"ids": request.paper_ids},
            cache_identity=identity,
            cache_values=request.model_dump(mode="json"),
        )

    def references(self, request: SemanticScholarPaperListLookup) -> SemanticScholarPaperResult:
        if request.context.dry_run:
            return self.fake.references(request)
        return self._paper_list(request, relation_key="citedPaper", endpoint="references")

    def citations(self, request: SemanticScholarPaperListLookup) -> SemanticScholarPaperResult:
        if request.context.dry_run:
            return self.fake.citations(request)
        return self._paper_list(request, relation_key="citingPaper", endpoint="citations")

    def recommendations(
        self, request: SemanticScholarRecommendationLookup
    ) -> SemanticScholarPaperResult:
        if request.context.dry_run:
            return self.fake.recommendations(request)
        identity = ",".join(request.paper_ids)
        cached = self._cached_result(request.context, identity, request.model_dump(mode="json"))
        if cached is not None:
            return self._paper_result(cached, cache_hit=True)
        return self._post_papers(
            request.context,
            "/recommendations/v1/papers/forpapers",
            params={"limit": request.limit, "fields": ",".join(request.fields)},
            json_body={"positivePaperIds": request.paper_ids},
            payload_path=("recommendedPapers",),
            cache_identity=identity,
            cache_values=request.model_dump(mode="json"),
        )

    def author(self, request: SemanticScholarAuthorLookup) -> SemanticScholarAuthorResult:
        if request.context.dry_run:
            return self.fake.author(request)
        cached = self._cached_result(
            request.context, request.author_id, request.model_dump(mode="json")
        )
        if cached is not None:
            return self._author_result(cached, cache_hit=True)
        guard = self._guard_live(request.context)
        if guard is not None:
            return SemanticScholarAuthorResult(status="error", error=guard)
        rate_error = RateLimitChecker(request.context.rate_limit).check(provider=PROVIDER)
        if rate_error is not None:
            return SemanticScholarAuthorResult(status="error", error=rate_error)
        result = self._request_json(
            request.context,
            "GET",
            f"/author/{request.author_id}",
            params={"fields": ",".join(request.fields)},
        )
        if isinstance(result, AdapterError):
            return SemanticScholarAuthorResult(status="error", error=result)
        payload: list[dict[str, object]] = [dict(result)]
        self._cache_result(
            request.context,
            request.author_id,
            request.model_dump(mode="json"),
            payload,
        )
        return self._author_result(payload)

    def _paper_list(
        self,
        request: SemanticScholarPaperListLookup,
        *,
        relation_key: str,
        endpoint: str,
    ) -> SemanticScholarPaperResult:
        cached = self._cached_result(request.context, endpoint, request.model_dump(mode="json"))
        if cached is not None:
            return self._paper_result(cached, cache_hit=True)
        result = self._get_papers(
            request.context,
            f"/paper/{request.paper_id}/{endpoint}",
            params={"limit": request.limit, "fields": ",".join(request.fields)},
            payload_path=("data",),
            cache_identity=endpoint,
            cache_values=request.model_dump(mode="json"),
            relation_key=relation_key,
        )
        return result

    def _get_papers(
        self,
        context: AdapterRequestContext,
        path: str,
        *,
        params: dict[str, object],
        payload_path: tuple[str, ...] | None = ("data",),
        cache_identity: str,
        cache_values: dict[str, Any],
        single: bool = False,
        relation_key: str | None = None,
    ) -> SemanticScholarPaperResult:
        guard = self._guard_live(context)
        if guard is not None:
            return SemanticScholarPaperResult(status="error", error=guard)
        rate_error = RateLimitChecker(context.rate_limit).check(provider=PROVIDER)
        if rate_error is not None:
            return SemanticScholarPaperResult(status="error", error=rate_error)
        result = self._request_json(context, "GET", path, params=params)
        if isinstance(result, AdapterError):
            return SemanticScholarPaperResult(status="error", error=result)
        papers = self._extract_papers(
            result, payload_path=payload_path, single=single, relation_key=relation_key
        )
        self._cache_result(context, cache_identity, cache_values, papers)
        return self._paper_result(papers)

    def _post_papers(
        self,
        context: AdapterRequestContext,
        path: str,
        *,
        params: dict[str, object],
        json_body: dict[str, object],
        payload_path: tuple[str, ...] | None = None,
        cache_identity: str,
        cache_values: dict[str, Any],
    ) -> SemanticScholarPaperResult:
        guard = self._guard_live(context)
        if guard is not None:
            return SemanticScholarPaperResult(status="error", error=guard)
        rate_error = RateLimitChecker(context.rate_limit).check(provider=PROVIDER)
        if rate_error is not None:
            return SemanticScholarPaperResult(status="error", error=rate_error)
        result = self._request_json(context, "POST", path, params=params, json_body=json_body)
        if isinstance(result, AdapterError):
            return SemanticScholarPaperResult(status="error", error=result)
        papers = self._extract_papers(result, payload_path=payload_path)
        self._cache_result(context, cache_identity, cache_values, papers)
        return self._paper_result(papers)

    def _request_json(
        self,
        context: AdapterRequestContext,
        method: str,
        path: str,
        *,
        params: dict[str, object],
        json_body: dict[str, object] | None = None,
    ) -> dict[str, Any] | list[Any] | AdapterError:
        httpx_module = self._httpx_module()
        if httpx_module is None:
            return self._error(
                AdapterErrorCode.UNSUPPORTED,
                "httpx is required for live Semantic Scholar calls",
            )
        timeout = httpx_module.Timeout(
            timeout=context.timeout.total_seconds,
            connect=context.timeout.connect_seconds,
            read=context.timeout.read_seconds,
            write=context.timeout.connect_seconds,
        )
        headers = self._headers()
        try:
            client_factory = self.client_factory or httpx_module.Client
            with client_factory(timeout=timeout, headers=headers) as client:
                response = client.request(
                    method,
                    f"{self.base_url}{path}",
                    params=params,
                    json=json_body,
                )
                response.raise_for_status()
                data = response.json()
        except httpx_module.TimeoutException as exc:
            return self._error(
                AdapterErrorCode.TIMEOUT,
                "Semantic Scholar request timed out",
                retryable=True,
                details={"exception": exc.__class__.__name__},
            )
        except httpx_module.HTTPStatusError as exc:
            return self._http_status_error(exc)
        except httpx_module.HTTPError as exc:
            return self._error(
                AdapterErrorCode.PROVIDER_ERROR,
                "Semantic Scholar provider request failed",
                retryable=True,
                details={"exception": exc.__class__.__name__},
            )
        except ValueError as exc:
            return self._error(
                AdapterErrorCode.INVALID_RESPONSE,
                "Semantic Scholar returned invalid JSON",
                details={"exception": exc.__class__.__name__},
            )
        if not isinstance(data, dict | list):
            return self._error(
                AdapterErrorCode.INVALID_RESPONSE,
                "Semantic Scholar response was not an object or list",
            )
        return data

    def _guard_live(self, context: AdapterRequestContext) -> AdapterError | None:
        if not context.live_enabled or context.default_enabled:
            return self._error(
                AdapterErrorCode.LIVE_DISABLED,
                "Semantic Scholar live adapter is disabled by default",
            )
        if context.dry_run:
            return self._error(
                AdapterErrorCode.LIVE_DISABLED,
                "Semantic Scholar request is dry-run",
            )
        if not os.getenv(self.api_key_env):
            return self._error(
                AdapterErrorCode.MISSING_API_KEY,
                "SEMANTIC_SCHOLAR_API_KEY is required for live Semantic Scholar calls",
            )
        return None

    def _headers(self) -> dict[str, str]:
        api_key = os.getenv(self.api_key_env)
        if not api_key:
            return {}
        return {"x-api-key": api_key}

    def _httpx_module(self) -> Any | None:
        if find_spec("httpx") is None:
            return None
        import httpx  # type: ignore[import-not-found]

        return httpx

    def _http_status_error(self, exc: Any) -> AdapterError:
        status_code = exc.response.status_code
        return self._http_status_code_error(status_code)

    def _http_status_code_error(self, status_code: int) -> AdapterError:
        if status_code == 429:
            return self._error(
                AdapterErrorCode.RATE_LIMITED,
                "Semantic Scholar rate limit reached",
                retryable=True,
                status_code=status_code,
            )
        if status_code in {401, 403}:
            return self._error(
                AdapterErrorCode.MISSING_API_KEY,
                "Semantic Scholar API key is missing or unauthorized",
                status_code=status_code,
            )
        return self._error(
            AdapterErrorCode.PROVIDER_ERROR,
            "Semantic Scholar provider returned an error",
            retryable=500 <= status_code <= 599,
            status_code=status_code,
        )

    def _extract_papers(
        self,
        payload: dict[str, Any] | list[Any],
        *,
        payload_path: tuple[str, ...] | None = None,
        single: bool = False,
        relation_key: str | None = None,
    ) -> list[dict[str, object]]:
        current: Any = payload
        if payload_path is not None:
            for item in payload_path:
                if not isinstance(current, dict):
                    return []
                current = current.get(item, [])
        if single:
            current = [current]
        if not isinstance(current, list):
            return []
        papers: list[dict[str, object]] = []
        for item in current:
            if not isinstance(item, dict):
                continue
            paper = item.get(relation_key) if relation_key else item
            if isinstance(paper, dict):
                papers.append(dict(paper))
        return papers

    def _paper_result(
        self, papers: list[dict[str, object]], *, cache_hit: bool = False
    ) -> SemanticScholarPaperResult:
        return SemanticScholarPaperResult(
            papers=papers,
            cache_hit=cache_hit,
            source_metadata=self._metadata(papers),
        )

    def _author_result(
        self, authors: list[dict[str, object]], *, cache_hit: bool = False
    ) -> SemanticScholarAuthorResult:
        return SemanticScholarAuthorResult(
            authors=authors,
            cache_hit=cache_hit,
            source_metadata=self._metadata(authors),
        )

    def _metadata(self, records: list[dict[str, object]]) -> list[SourceMetadata]:
        source_id = None
        url = None
        if records:
            first = records[0]
            source_id_value = first.get("paperId") or first.get("paper_id") or first.get("authorId")
            source_id = str(source_id_value or "")
            url_value = first.get("url")
            url = str(url_value) if url_value else None
        return [
            SourceMetadata(
                provider=PROVIDER,
                source_id=source_id or None,
                url=url,
                retrieval_time=datetime.now(UTC),
                human_verified=False,
            )
        ]

    def _cached_result(
        self,
        context: AdapterRequestContext,
        identity: str,
        values: dict[str, Any],
    ) -> list[dict[str, object]] | None:
        key = build_adapter_cache_key(context.cache, identity, values)
        cached = self.cache.get(key)
        records = cached.get("records") if cached else None
        if isinstance(records, list):
            return [dict(item) for item in records if isinstance(item, dict)]
        return None

    def _cache_result(
        self,
        context: AdapterRequestContext,
        identity: str,
        values: dict[str, Any],
        records: list[dict[str, object]],
    ) -> None:
        if not context.cache.write_through:
            return
        key = build_adapter_cache_key(context.cache, identity, values)
        self.cache.put(key, {"records": records})

    def _error(
        self,
        code: AdapterErrorCode,
        message: str,
        *,
        retryable: bool = False,
        status_code: int | None = None,
        details: dict[str, str] | None = None,
    ) -> AdapterError:
        return AdapterError(
            code=code,
            message=message,
            retryable=retryable,
            provider=PROVIDER,
            status_code=status_code,
            details=details or {},
        )


__all__ = ["DEFAULT_BASE_URL", "PROVIDER", "SemanticScholarLiveAdapter"]
