from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import web_fetch_live_skip_reason
from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import RetrievalStatus, WebFetchRequest


@pytest.mark.live
def test_web_fetch_live_optional() -> None:
    reason = web_fetch_live_skip_reason()
    if reason is not None:
        pytest.skip(reason)

    result = WebFetcher().fetch(
        WebFetchRequest(
            url="https://example.com",
            dry_run=False,
            live_enabled=True,
        )
    )

    assert result.retrieval_status in {RetrievalStatus.RETRIEVED, RetrievalStatus.ERROR}
    assert result.source_metadata.human_verified is False
