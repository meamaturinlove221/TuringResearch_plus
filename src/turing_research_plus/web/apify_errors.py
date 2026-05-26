"""Typed Apify adapter errors."""

from __future__ import annotations

from turing_research_plus.adapters.errors import AdapterError, AdapterErrorCode

PROVIDER = "apify"


def apify_error(
    code: AdapterErrorCode | str,
    message: str,
    *,
    retryable: bool = False,
    status_code: int | None = None,
) -> AdapterError:
    """Create a typed Apify error."""

    return AdapterError(
        code=str(code),
        message=message,
        retryable=retryable,
        provider=PROVIDER,
        status_code=status_code,
        details={},
    )
