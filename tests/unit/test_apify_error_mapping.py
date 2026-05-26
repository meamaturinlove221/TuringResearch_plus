from __future__ import annotations

from turing_research_plus.adapters.errors import AdapterErrorCode
from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunStatus


def test_apify_missing_token_returns_typed_error(monkeypatch) -> None:
    monkeypatch.delenv("APIFY_TOKEN", raising=False)

    result = ApifyAdapter().run(
        ApifyRunRequest(
            actor_id="public/actor",
            input={"url": "https://example.com"},
            dry_run=False,
            live_enabled=True,
        )
    )

    assert result.status == ApifyRunStatus.MISSING_TOKEN
    assert result.errors[0].code == AdapterErrorCode.MISSING_API_KEY


def test_apify_live_disabled_returns_typed_error() -> None:
    result = ApifyAdapter().run(
        ApifyRunRequest(
            actor_id="public/actor",
            input={"url": "https://example.com"},
            dry_run=False,
            live_enabled=False,
        )
    )

    assert result.status == ApifyRunStatus.LIVE_DISABLED
    assert result.errors[0].code == AdapterErrorCode.LIVE_DISABLED
