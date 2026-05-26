from __future__ import annotations

from turing_research_plus.adapters.errors import AdapterErrorCode
from turing_research_plus.adapters.models import SemanticScholarPaperIdLookup
from turing_research_plus.adapters.semantic_scholar import SemanticScholarLiveAdapter


def test_live_adapter_returns_live_disabled_by_default() -> None:
    adapter = SemanticScholarLiveAdapter()
    request = SemanticScholarPaperIdLookup(paper_id="S2-1")
    request.context.dry_run = False

    result = adapter.paper_lookup_by_id(request)

    assert result.status == "error"
    assert result.error is not None
    assert result.error.code == AdapterErrorCode.LIVE_DISABLED


def test_live_adapter_missing_key_is_typed_error(monkeypatch) -> None:
    monkeypatch.delenv("SEMANTIC_SCHOLAR_API_KEY", raising=False)
    adapter = SemanticScholarLiveAdapter()
    request = SemanticScholarPaperIdLookup(paper_id="S2-1")
    request.context.dry_run = False
    request.context.live_enabled = True

    result = adapter.paper_lookup_by_id(request)

    assert result.status == "error"
    assert result.error is not None
    assert result.error.code == AdapterErrorCode.MISSING_API_KEY


def test_http_status_error_maps_rate_limit() -> None:
    adapter = SemanticScholarLiveAdapter()

    mapped = adapter._http_status_code_error(429)

    assert mapped.code == AdapterErrorCode.RATE_LIMITED
    assert mapped.retryable is True
    assert mapped.status_code == 429
