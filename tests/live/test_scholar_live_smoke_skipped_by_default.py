from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import (
    LIVE_TEST_ENV,
    SEMANTIC_SCHOLAR_API_KEY_ENV,
    semantic_scholar_live_skip_reason,
)


@pytest.mark.live
def test_scholar_live_smoke_skipped_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv(LIVE_TEST_ENV, raising=False)
    monkeypatch.delenv("TURINGRESEARCH_ENABLE_SEMANTIC_SCHOLAR_LIVE", raising=False)
    monkeypatch.delenv(SEMANTIC_SCHOLAR_API_KEY_ENV, raising=False)

    reason = semantic_scholar_live_skip_reason()
    if reason is not None:
        pytest.skip(reason)

    pytest.fail("Scholar live smoke should skip without explicit live opt-in")
