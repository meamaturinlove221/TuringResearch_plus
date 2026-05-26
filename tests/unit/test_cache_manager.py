import pytest
from pydantic import ValidationError

from turing_research.cache.keys import build_cache_key
from turing_research.cache.manager import CacheEntry, CacheManager


def test_cache_manager_writes_sha256_filename(tmp_path) -> None:
    manager = CacheManager(tmp_path)
    key = build_cache_key("source", "https://example.com/item")

    manager.put(key, {"title": "cached"}, {"source": "unit-test"})

    path = manager.path_for(key)
    assert path.name == f"{key}.json"
    assert "example.com" not in path.name
    assert manager.exists(key) is True


def test_cache_manager_reads_entry_with_metadata(tmp_path) -> None:
    manager = CacheManager(tmp_path)
    key = build_cache_key("source", "id-1")
    manager.put(key, {"value": 1}, {"artifact_id": "artifact-1"})

    entry = manager.get(key)

    assert entry is not None
    assert entry.metadata == {"artifact_id": "artifact-1"}
    assert entry.value == {"value": 1}


def test_cache_entry_requires_metadata() -> None:
    key = build_cache_key("source", "id-1")

    with pytest.raises(ValidationError):
        CacheEntry(key=key, value={}, metadata={})


def test_cache_manager_rejects_non_sha256_path(tmp_path) -> None:
    manager = CacheManager(tmp_path)

    with pytest.raises(ValueError):
        manager.path_for("https://example.com/raw-url")
