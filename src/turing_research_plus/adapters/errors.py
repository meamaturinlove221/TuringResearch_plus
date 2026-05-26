"""Typed live adapter errors for TuringResearch Plus."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AdapterErrorCode(StrEnum):
    """Stable adapter error code constants."""

    MISSING_API_KEY = "missing_api_key"
    TIMEOUT = "timeout"
    RATE_LIMITED = "rate_limited"
    RETRY_EXHAUSTED = "retry_exhausted"
    PROVIDER_ERROR = "provider_error"
    INVALID_RESPONSE = "invalid_response"
    UNSUPPORTED = "unsupported"
    SOURCE_HYGIENE_BLOCKED = "source_hygiene_blocked"
    LIVE_DISABLED = "live_disabled"


class AdapterError(BaseModel):
    """Typed error returned by adapter boundaries."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1)
    message: str = Field(min_length=1)
    retryable: bool = False
    provider: str | None = None
    status_code: int | None = Field(default=None, ge=100, le=599)
    details: dict[str, str] = Field(default_factory=dict)
