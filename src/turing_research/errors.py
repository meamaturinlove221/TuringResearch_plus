"""Shared Core errors."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ErrorCode(StrEnum):
    """Stable Core error codes."""

    CACHE_MISS = "cache_miss"
    INVALID_CACHE_ENTRY = "invalid_cache_entry"
    REGISTRY_READ_FAILED = "registry_read_failed"


class CoreError(BaseModel):
    """Serializable Core error."""

    model_config = ConfigDict(extra="forbid")

    code: ErrorCode
    message: str = Field(min_length=1)
