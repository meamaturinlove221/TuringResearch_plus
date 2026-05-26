from __future__ import annotations

from turing_research_plus.web import build_apify_usage_guide
from turing_research_plus.web_tools import (
    WebContentSurfaceRequest,
    WebFetchingSurfaceRequest,
    build_web_full_tool_surface,
    build_web_source_metadata_report,
    inspect_web_cache,
    run_web_content_surface,
    run_web_fetching_surface,
)


def test_web_full_tool_surface_fake_workflow() -> None:
    surface = build_web_full_tool_surface()
    fetching = run_web_fetching_surface(
        WebFetchingSurfaceRequest(url="https://example.com/public-page")
    )
    content = run_web_content_surface(
        WebContentSurfaceRequest(url="https://example.com/public-page")
    )
    cache = inspect_web_cache("https://example.com/public-page")
    metadata = build_web_source_metadata_report(
        source_url="https://example.com/public-page",
        content="Fake public page content",
    )
    apify = build_apify_usage_guide()

    assert surface.release_blocker is False
    assert fetching.retrieval_status == "dry-run"
    assert fetching.default_network is False
    assert content.human_verified is False
    assert content.promoted_to_evidence is False
    assert cache.stores_cookies is False
    assert metadata.human_verified is False
    assert apify.default_live_enabled is False
    assert apify.stores_cookies is False
    assert apify.bypasses_paywall is False
    assert apify.fetches_private_content is False
    assert all(tool.requires_human_review for tool in surface.tools)


def test_web_full_tool_surface_fake_workflow_has_no_unsafe_defaults() -> None:
    surface = build_web_full_tool_surface()

    assert surface.fake_mode_default is True
    assert surface.live_tests_skipped_by_default is True
    assert surface.default_network is False
    assert surface.stores_cookies is False
    assert surface.paywall_bypass_allowed is False
    assert surface.private_content_fetching_allowed is False
    assert surface.automatic_evidence_promotion is False
    assert all(not tool.requires_api_key for tool in surface.tools)
    assert all(not tool.stores_cookies for tool in surface.tools)
    assert all(not tool.fetches_private_content for tool in surface.tools)
    assert all(not tool.bypasses_paywall for tool in surface.tools)
    assert all(not tool.promotes_to_verified_evidence for tool in surface.tools)
