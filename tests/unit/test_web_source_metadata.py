from __future__ import annotations

from turing_research_plus.web.source_metadata import (
    build_cache_key,
    build_source_metadata,
    hash_text,
)


def test_source_metadata_uses_hash_and_not_verified() -> None:
    metadata = build_source_metadata(
        source_url="https://example.com/source",
        content="hello",
    )

    assert metadata.content_hash == hash_text("hello")
    assert metadata.source_url == "https://example.com/source"
    assert metadata.human_verified is False
    assert build_cache_key("https://example.com/source") != "https://example.com/source"
