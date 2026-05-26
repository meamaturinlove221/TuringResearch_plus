from __future__ import annotations

from turing_research_plus.run_ingest.models import BackendStatus, RunStatus
from turing_research_plus.run_ingest.status_parser import parse_backend_status, parse_run_status


def test_parse_run_status_recognizes_required_labels() -> None:
    assert parse_run_status("REVIEW_READY_NOT_PROMOTED") == RunStatus.REVIEW_READY_NOT_PROMOTED
    assert parse_run_status("route exhausted with failure analysis") == (
        RunStatus.ROUTE_EXHAUSTED_WITH_FAILURE_ANALYSIS
    )
    assert parse_run_status("hard-blocked") == RunStatus.HARD_BLOCKED
    assert parse_run_status("failed") == RunStatus.RUN_FAILED
    assert parse_run_status("partial") == RunStatus.PARTIAL
    assert parse_run_status(None) == RunStatus.UNKNOWN


def test_parse_backend_status_is_conservative() -> None:
    assert parse_backend_status("real backend confirmed") == BackendStatus.REAL_BACKEND_CONFIRMED
    assert parse_backend_status("sparse backend unavailable") == BackendStatus.REAL_BACKEND_MISSING
    assert parse_backend_status("fallback backend used") == BackendStatus.FALLBACK_USED
    assert parse_backend_status(None) == BackendStatus.UNKNOWN
