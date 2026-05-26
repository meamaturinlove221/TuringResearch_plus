from __future__ import annotations

import pytest

from turing_research_plus.web_tools import (
    WebContentSurfaceRequest,
    build_web_source_metadata_report,
    inspect_web_cache,
    run_web_content_surface,
)


def test_web_content_surface_returns_review_context() -> None:
    result = run_web_content_surface(
        WebContentSurfaceRequest(url="https://example.com/public-page")
    )

    assert result.tool_name == "web.web_content"
    assert result.text_preview is not None
    assert result.human_verified is False
    assert result.promoted_to_evidence is False
    assert result.requires_human_review is True
    assert result.release_blocker is False


def test_web_content_surface_rejects_overpromotion() -> None:
    with pytest.raises(ValueError, match="live fetch"):
        WebContentSurfaceRequest(url="https://example.com", live_enabled=True)
    with pytest.raises(ValueError, match="human verified"):
        WebContentSurfaceRequest(url="https://example.com", human_verified=True)
    with pytest.raises(ValueError, match="auto-promote"):
        WebContentSurfaceRequest(url="https://example.com", promote_to_evidence=True)


def test_web_cache_and_source_metadata_surfaces_are_review_only() -> None:
    cache = inspect_web_cache("https://example.com/public-page")
    metadata = build_web_source_metadata_report(
        source_url="https://example.com/public-page",
        content="Fake public page content",
    )

    assert cache.status == "miss"
    assert cache.persistent_storage is False
    assert cache.stores_cookies is False
    assert cache.contains_private_content is False
    assert cache.release_blocker is False
    assert metadata.human_verified is False
    assert metadata.requires_human_review is True
    assert metadata.release_blocker is False
