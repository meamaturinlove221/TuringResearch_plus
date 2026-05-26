from __future__ import annotations

from turing_research_plus.web import (
    WebFetchingToolRequest,
    build_apify_usage_guide,
    run_web_fetching_tool,
)
from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunStatus
from turing_research_plus.web.models import RetrievalStatus
from turing_research_plus.web.web_content_tool import web_content_from_fetch_result


def test_neocortica_web_parity_fake_flow_is_no_network_and_review_only(monkeypatch) -> None:
    monkeypatch.delenv("APIFY_TOKEN", raising=False)

    fetching = run_web_fetching_tool(
        WebFetchingToolRequest(url="https://example.com/public-page")
    )
    content = web_content_from_fetch_result(fetching.fetch_result)
    apify_guide = build_apify_usage_guide()
    apify_result = ApifyAdapter().run(
        ApifyRunRequest(
            actor_id="apify/fake",
            input={"url": "https://example.com/public-page"},
            dry_run=False,
            live_enabled=True,
        )
    )

    assert fetching.fetch_result.retrieval_status == RetrievalStatus.DRY_RUN
    assert fetching.default_network is False
    assert content.human_verified is False
    assert content.requires_human_review is True
    assert apify_guide.default_live_enabled is False
    assert apify_result.status == ApifyRunStatus.MISSING_TOKEN
    assert apify_result.requires_human_review is True
