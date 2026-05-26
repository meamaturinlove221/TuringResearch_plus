"""Status parsing for run ingestor fixtures."""

from __future__ import annotations

from turing_research_plus.run_ingest.models import BackendStatus, RunStatus


def parse_run_status(value: str | None) -> RunStatus:
    """Parse run status conservatively."""

    if not value:
        return RunStatus.UNKNOWN
    normalized = value.strip().upper().replace("-", "_").replace(" ", "_")
    for status in RunStatus:
        if normalized == status.value:
            return status
    if "HARD_BLOCK" in normalized:
        return RunStatus.HARD_BLOCKED
    if "FAILED" in normalized:
        return RunStatus.RUN_FAILED
    if "PARTIAL" in normalized:
        return RunStatus.PARTIAL
    if "REVIEW_READY" in normalized:
        return RunStatus.REVIEW_READY_NOT_PROMOTED
    return RunStatus.UNKNOWN


def parse_backend_status(value: str | None) -> BackendStatus:
    """Parse sparse backend status."""

    if not value:
        return BackendStatus.UNKNOWN
    normalized = value.strip().lower().replace("-", "_").replace(" ", "_")
    for status in BackendStatus:
        if normalized == status.value:
            return status
    if "fallback" in normalized:
        return BackendStatus.FALLBACK_USED
    if "missing" in normalized or "unavailable" in normalized:
        return BackendStatus.REAL_BACKEND_MISSING
    if "confirmed" in normalized or "real" in normalized:
        return BackendStatus.REAL_BACKEND_CONFIRMED
    return BackendStatus.UNKNOWN
