from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import (
    APIFY_TOKEN_ENV,
    LIVE_TEST_ENV,
    apify_live_skip_reason,
    web_fetch_live_skip_reason,
)


@pytest.mark.live
def test_web_apify_live_smoke_skipped_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(LIVE_TEST_ENV, raising=False)
    monkeypatch.delenv("TURINGRESEARCH_ENABLE_WEB_LIVE", raising=False)
    monkeypatch.delenv("TURINGRESEARCH_ENABLE_APIFY_LIVE", raising=False)
    monkeypatch.delenv(APIFY_TOKEN_ENV, raising=False)

    web_reason = web_fetch_live_skip_reason()
    apify_reason = apify_live_skip_reason()
    if web_reason is not None or apify_reason is not None:
        pytest.skip(web_reason or apify_reason)

    pytest.fail("Web / Apify live smoke should skip without explicit live opt-in")
