from __future__ import annotations

from turing_research_plus.web.models import SourceType, WebFetchRequest


def test_web_fetch_request_defaults_to_dry_run() -> None:
    request = WebFetchRequest(url="https://example.com/project")

    assert request.dry_run is True
    assert request.live_enabled is False
    assert request.source_type == SourceType.PUBLIC_WEB
    assert request.source_hygiene_status == "public_or_authorized"
