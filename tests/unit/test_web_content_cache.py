from __future__ import annotations

from turing_research_plus.web.content_cache import WebContentCache
from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import RetrievalStatus, WebFetchRequest


def test_web_content_cache_records_hit() -> None:
    cache = WebContentCache()
    fetcher = WebFetcher(cache=cache)
    request = WebFetchRequest(url="https://example.com/cache")

    first = fetcher.fetch(request)
    second = fetcher.fetch(request)

    assert first.retrieval_status == RetrievalStatus.DRY_RUN
    assert second.retrieval_status == RetrievalStatus.CACHE_HIT
    assert second.cache_hit is True
    assert cache.cache_status("https://example.com/cache") == "hit"
