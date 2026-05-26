from __future__ import annotations

import pytest

from turing_research_plus.web_tools import (
    WebFetchingSurfaceRequest,
    run_web_fetching_surface,
)


def test_web_fetching_surface_runs_fake_default() -> None:
    result = run_web_fetching_surface(
        WebFetchingSurfaceRequest(url="https://example.com/public-page")
    )

    assert result.tool_name == "web.web_fetching"
    assert result.retrieval_status == "dry-run"
    assert result.source_type == "fake"
    assert result.default_network is False
    assert result.live_enabled is False
    assert result.stores_cookies is False
    assert result.requires_api_key is False
    assert result.requires_human_review is True
    assert result.release_blocker is False


def test_web_fetching_surface_rejects_unsafe_options() -> None:
    with pytest.raises(ValueError, match="live mode"):
        WebFetchingSurfaceRequest(
            url="https://example.com/public-page",
            live_enabled=True,
            dry_run=False,
        )
    with pytest.raises(ValueError, match="store cookies"):
        WebFetchingSurfaceRequest(
            url="https://example.com/public-page",
            stores_cookies=True,
        )
    with pytest.raises(ValueError, match="private content"):
        WebFetchingSurfaceRequest(
            url="https://example.com/public-page",
            fetches_private_content=True,
        )
    with pytest.raises(ValueError, match="paywalls"):
        WebFetchingSurfaceRequest(
            url="https://example.com/public-page",
            bypasses_paywall=True,
        )
