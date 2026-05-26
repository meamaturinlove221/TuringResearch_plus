"""Local tool wrappers for web fetch and Apify adapters."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.web.apify import ApifyAdapter
from turing_research_plus.web.apify_models import ApifyRunRequest, ApifyRunResult
from turing_research_plus.web.fetcher import WebFetcher
from turing_research_plus.web.models import SourceType, WebFetchRequest, WebFetchResult


def web_fetch(
    url: str,
    *,
    fixture_path: str | None = None,
    live_enabled: bool = False,
    dry_run: bool = True,
) -> WebFetchResult:
    """Fetch public web content through fake/default or explicit live mode."""

    request = WebFetchRequest(
        url=url,
        fixture_path=Path(fixture_path) if fixture_path else None,
        live_enabled=live_enabled,
        dry_run=dry_run,
        source_type=SourceType.LOCAL_FIXTURE if fixture_path else SourceType.PUBLIC_WEB,
    )
    return WebFetcher().fetch(request)


def apify_run_optional(
    *,
    actor_id: str | None = None,
    input: dict[str, object] | None = None,
    live_enabled: bool = False,
    dry_run: bool = True,
) -> ApifyRunResult:
    """Run optional Apify adapter with fake/default behavior."""

    request = ApifyRunRequest(
        actor_id=actor_id,
        input=input or {},
        live_enabled=live_enabled,
        dry_run=dry_run,
    )
    return ApifyAdapter().run(request)
