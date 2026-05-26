from __future__ import annotations

from turing_research_plus.web import build_apify_usage_guide, render_apify_usage_guide
from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunStatus


def test_apify_usage_guide_is_live_optional_and_public_safe() -> None:
    guide = build_apify_usage_guide()

    assert guide.default_live_enabled is False
    assert guide.apify_live_env == "TURINGRESEARCH_ENABLE_APIFY_LIVE=0"
    assert guide.live_tests_env == "TURINGRESEARCH_ENABLE_LIVE_TESTS=0"
    assert guide.token_env == "APIFY_TOKEN"
    assert guide.stores_cookies is False
    assert guide.bypasses_paywall is False
    assert guide.fetches_private_content is False
    assert guide.release_blocker is False


def test_apify_missing_key_is_graceful_skip(monkeypatch) -> None:
    monkeypatch.delenv("APIFY_TOKEN", raising=False)
    result = ApifyAdapter().run(
        ApifyRunRequest(
            actor_id="apify/fake",
            input={"url": "https://example.com"},
            dry_run=False,
            live_enabled=True,
        )
    )

    assert result.status == ApifyRunStatus.MISSING_TOKEN
    assert result.requires_human_review is True
    assert result.errors


def test_render_apify_usage_guide_mentions_no_key_behavior() -> None:
    rendered = render_apify_usage_guide(build_apify_usage_guide())

    assert "Default live enabled: `false`" in rendered
    assert "No-key behavior: graceful missing-token result" in rendered
    assert "Token env: `APIFY_TOKEN`" in rendered
