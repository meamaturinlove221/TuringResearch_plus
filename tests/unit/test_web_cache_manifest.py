from __future__ import annotations

from datetime import UTC, datetime

import pytest

from turing_research_plus.web.content_cache import WebContentCache
from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import RetrievalStatus, WebFetchRequest
from turing_research_plus.web_tools import (
    WebCacheLiveStatus,
    WebCacheManifestEntry,
    build_web_cache_manifest,
    build_web_cache_manifest_entry,
    manifest_entry_from_cache_record,
    normalize_url,
)


def test_cache_manifest_tracks_source_url_fetch_time_hash_and_fake_status() -> None:
    fetch_time = datetime(2026, 5, 22, 8, 30, tzinfo=UTC)

    entry = build_web_cache_manifest_entry(
        source_url="HTTPS://Example.COM:443/path?utm_source=x&b=2&a=1#frag",
        content="fake cached content",
        fetch_time=fetch_time,
    )

    assert entry.source_url == "HTTPS://Example.COM:443/path?utm_source=x&b=2&a=1#frag"
    assert entry.normalized_url == "https://example.com/path?a=1&b=2"
    assert entry.cache_key == normalize_url(entry.source_url).cache_key
    assert entry.fetch_time == fetch_time
    assert len(entry.content_hash) == 64
    assert entry.retrieval_status == RetrievalStatus.DRY_RUN
    assert entry.live_status == WebCacheLiveStatus.FAKE
    assert entry.network_used is False
    assert entry.requires_human_review is True
    assert entry.release_blocker is False


def test_cache_manifest_collects_entries_and_keeps_live_network_disabled_by_default() -> None:
    entry = build_web_cache_manifest_entry(
        source_url="https://example.com/cache",
        content="cached content",
    )

    manifest = build_web_cache_manifest([entry])

    assert manifest.manifest_version == "v1.4-web-cache-manifest"
    assert manifest.fake_mode_default is True
    assert manifest.live_network_default is False
    assert manifest.cookie_storage_enabled is False
    assert manifest.entries == [entry]
    assert manifest.release_blocker is False


def test_manifest_entry_from_cache_record_preserves_cached_metadata() -> None:
    cache = WebContentCache()
    fetcher = WebFetcher(cache=cache)
    request = WebFetchRequest(url="https://example.com/cache-manifest")

    result = fetcher.fetch(request)
    cache.put_result(result, manual_fixture_mode=True)
    record = cache.get("https://example.com/cache-manifest")

    assert record is not None
    entry = manifest_entry_from_cache_record(record)

    assert entry.source_url == "https://example.com/cache-manifest"
    assert entry.normalized_url == "https://example.com/cache-manifest"
    assert entry.retrieval_status == RetrievalStatus.CACHE_HIT
    assert entry.live_status == WebCacheLiveStatus.CACHE_ONLY
    assert entry.fetch_time == record.retrieval_time
    assert entry.network_used is False
    assert entry.release_blocker is False


def test_cache_manifest_rejects_unsafe_or_misleading_entries() -> None:
    base = {
        "source_url": "https://example.com",
        "normalized_url": "https://example.com/",
        "fetch_time": datetime(2026, 5, 22, tzinfo=UTC),
        "content_hash": "a" * 64,
        "cache_key": "b" * 64,
    }

    with pytest.raises(ValueError, match="require human review"):
        WebCacheManifestEntry(**base, requires_human_review=False)
    with pytest.raises(ValueError, match="not human verified"):
        WebCacheManifestEntry(**base, human_verified=True)
    with pytest.raises(ValueError, match="must not store cookies"):
        WebCacheManifestEntry(**base, stores_cookies=True)
    with pytest.raises(ValueError, match="must not contain private content"):
        WebCacheManifestEntry(**base, contains_private_content=True)
    with pytest.raises(ValueError, match="network_used requires live status"):
        WebCacheManifestEntry(**base, network_used=True)
