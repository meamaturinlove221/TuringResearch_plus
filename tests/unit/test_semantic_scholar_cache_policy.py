from __future__ import annotations

from turing_research.cache.keys import is_sha256_key
from turing_research_plus.adapters.cache import InMemoryAdapterCache, build_adapter_cache_key
from turing_research_plus.adapters.models import SemanticScholarPaperIdLookup
from turing_research_plus.adapters.rate_limit import RateLimitChecker


def test_adapter_cache_uses_sha256_keys() -> None:
    request = SemanticScholarPaperIdLookup(paper_id="CorpusId:123")

    key = build_adapter_cache_key(
        request.context.cache,
        request.paper_id,
        request.model_dump(mode="json"),
    )

    assert is_sha256_key(str(key))
    assert "CorpusId" not in str(key)


def test_in_memory_adapter_cache_round_trip() -> None:
    cache = InMemoryAdapterCache()
    request = SemanticScholarPaperIdLookup(paper_id="S2-1")
    key = build_adapter_cache_key(
        request.context.cache,
        request.paper_id,
        request.model_dump(mode="json"),
    )

    cache.put(key, {"records": [{"paperId": "S2-1"}]})

    assert cache.exists(key)
    assert cache.get(key) == {"records": [{"paperId": "S2-1"}]}


def test_rate_limit_placeholder_returns_typed_error() -> None:
    request = SemanticScholarPaperIdLookup(paper_id="S2-1")
    request.context.rate_limit.requests_per_minute = 1
    checker = RateLimitChecker(request.context.rate_limit)

    assert checker.check(provider="semantic_scholar") is None
    error = checker.check(provider="semantic_scholar")

    assert error is not None
    assert error.code == "rate_limited"
