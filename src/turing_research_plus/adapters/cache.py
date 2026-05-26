"""Small adapter cache helpers with hashed keys."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from turing_research.cache.keys import CacheKey, build_cache_key, is_sha256_key
from turing_research_plus.adapters.models import AdapterCachePolicy


def build_adapter_cache_key(
    policy: AdapterCachePolicy,
    identity: str,
    values: Mapping[str, Any],
) -> CacheKey:
    """Build a sha256 cache key from declared policy fields."""

    params = {field_name: values.get(field_name) for field_name in policy.cache_key_fields}
    return build_cache_key(policy.namespace, identity, params)


@dataclass
class InMemoryAdapterCache:
    """Deterministic process-local cache for adapter unit tests and dry-runs."""

    entries: dict[str, dict[str, Any]] = field(default_factory=dict)

    def get(self, key: CacheKey | str) -> dict[str, Any] | None:
        key_text = str(key)
        if not is_sha256_key(key_text):
            raise ValueError("adapter cache key must be a sha256 digest")
        return self.entries.get(key_text)

    def put(self, key: CacheKey | str, value: dict[str, Any]) -> None:
        key_text = str(key)
        if not is_sha256_key(key_text):
            raise ValueError("adapter cache key must be a sha256 digest")
        self.entries[key_text] = value

    def exists(self, key: CacheKey | str) -> bool:
        return self.get(key) is not None
