from __future__ import annotations

from turing_research_plus.scholar_pipeline import (
    ScholarFallbackStatus,
    build_scholar_fallback_policy,
    render_scholar_fallback_policy,
)


def test_scholar_fallback_policy_blocks_heavy_and_unsafe_paths() -> None:
    policy = build_scholar_fallback_policy()
    by_source = {rule.source: rule for rule in policy.rules}

    assert by_source["cached_markdown"].status == ScholarFallbackStatus.ALLOWED
    assert by_source["known_arxiv_metadata"].status == ScholarFallbackStatus.ALLOWED
    assert by_source["semantic_scholar_fake_or_live"].requires_live_opt_in is True
    assert by_source["mineru_heavy_pdf_fallback"].status == ScholarFallbackStatus.DEFERRED
    assert by_source["paywall_bypass"].status == ScholarFallbackStatus.REJECTED
    assert by_source["automatic_full_paper_download"].status == ScholarFallbackStatus.REJECTED
    assert policy.release_blocker is False
    assert policy.heavy_ocr_allowed is False


def test_render_scholar_fallback_policy_is_explicit() -> None:
    rendered = render_scholar_fallback_policy(build_scholar_fallback_policy())

    assert "Paywall bypass allowed: `false`" in rendered
    assert "`mineru_heavy_pdf_fallback`" in rendered
    assert "`deferred`" in rendered
