"""Cache key helpers."""

from __future__ import annotations

import hashlib
import json
from typing import Any, NewType

CacheKey = NewType("CacheKey", str)


def _canonical_payload(namespace: str, identity: str, params: dict[str, Any] | None) -> bytes:
    payload = {
        "identity": identity,
        "namespace": namespace,
        "params": params or {},
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
        "utf-8"
    )


def build_cache_key(
    namespace: str,
    identity: str,
    params: dict[str, Any] | None = None,
) -> CacheKey:
    """Build a stable sha256 cache key without exposing URL text as a filename."""

    if not namespace:
        raise ValueError("namespace is required")
    if not identity:
        raise ValueError("identity is required")

    digest = hashlib.sha256(_canonical_payload(namespace, identity, params)).hexdigest()
    return CacheKey(digest)


def is_sha256_key(value: str) -> bool:
    """Return whether a value is a lowercase sha256 hex digest."""

    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)
