from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import (
    LIVE_TEST_ENV,
    apify_live_skip_reason,
)


@pytest.mark.live
def test_apify_live_is_skipped_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(LIVE_TEST_ENV, raising=False)
    monkeypatch.delenv("APIFY_TOKEN", raising=False)

    reason = apify_live_skip_reason()
    if reason is not None:
        pytest.skip(reason)

    pytest.fail("Apify live test should be skipped without explicit live opt-in")
