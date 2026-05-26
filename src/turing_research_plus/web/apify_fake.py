"""Fake Apify adapter for default tests."""

from __future__ import annotations

from datetime import UTC, datetime

from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunResult, ApifyRunStatus


class FakeApifyAdapter:
    """Return deterministic Apify-shaped output without network access."""

    def run(self, request: ApifyRunRequest) -> ApifyRunResult:
        actor_id = request.actor_id or "fake/web-fetch"
        return ApifyRunResult(
            actor_id=actor_id,
            run_id="fake-apify-run-001",
            status=ApifyRunStatus.DRY_RUN,
            input=request.input,
            output_items=[
                {
                    "url": str(request.input.get("url", "https://example.com/fake")),
                    "title": "Fake Apify result",
                    "text": "Fake Apify output; retrieved is not verified.",
                    "human_verified": False,
                }
            ],
            retrieved_at=datetime(2026, 5, 20, tzinfo=UTC),
            warnings=["fake/default mode; no Apify request performed"],
            errors=[],
            requires_human_review=True,
        )
