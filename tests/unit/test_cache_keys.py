from turing_research.cache.keys import build_cache_key, is_sha256_key


def test_cache_key_is_sha256_digest() -> None:
    key = build_cache_key("web", "https://example.com/path?a=1", {"mode": "dry-run"})

    assert is_sha256_key(key)
    assert len(key) == 64


def test_cache_key_does_not_expose_url_text() -> None:
    key = build_cache_key("web", "https://example.com/private/path")

    assert "example.com" not in key
    assert "/" not in key
    assert ":" not in key


def test_cache_key_is_stable_for_canonical_params() -> None:
    left = build_cache_key("web", "id", {"b": 2, "a": 1})
    right = build_cache_key("web", "id", {"a": 1, "b": 2})

    assert left == right
