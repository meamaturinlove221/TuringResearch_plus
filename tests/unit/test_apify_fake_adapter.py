from __future__ import annotations

from turing_research_plus.web.apify_fake import FakeApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunStatus


def test_fake_apify_adapter_returns_deterministic_output() -> None:
    result = FakeApifyAdapter().run(
        ApifyRunRequest(actor_id="fake/actor", input={"url": "https://example.com"})
    )

    assert result.status == ApifyRunStatus.DRY_RUN
    assert result.actor_id == "fake/actor"
    assert result.run_id == "fake-apify-run-001"
    assert result.output_items[0]["human_verified"] is False
    assert result.requires_human_review is True
