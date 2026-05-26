from __future__ import annotations

from turing_research_plus.web.apify_models import ApifyRunRequest


def test_apify_request_defaults_to_dry_run() -> None:
    request = ApifyRunRequest(input={"url": "https://example.com"})

    assert request.dry_run is True
    assert request.live_enabled is False
    assert request.actor_id is None
