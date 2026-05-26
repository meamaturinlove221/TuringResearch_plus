from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import apify_live_skip_reason
from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunStatus


@pytest.mark.live
def test_apify_live_optional() -> None:
    reason = apify_live_skip_reason()
    if reason is not None:
        pytest.skip(reason)

    result = ApifyAdapter().run(
        ApifyRunRequest(
            actor_id="apify/web-scraper",
            input={"startUrls": [{"url": "https://example.com"}], "maxRequestsPerCrawl": 1},
            dry_run=False,
            live_enabled=True,
        )
    )

    assert result.status in {ApifyRunStatus.SUCCEEDED, ApifyRunStatus.ERROR}
    assert result.requires_human_review is True
