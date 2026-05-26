"""Small JSON cache manager for shared Core cache entries."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from tuling_research.cache.keys import CacheKey, is_sha256_key


class CacheEntry(BaseModel):
    """A cache entry with required metadata."""

    model_config = ConfigDict(extra="forbid")

    key: CacheKey
    value: dict[str, Any]
    metadata: dict[str, Any] = Field(min_length=1)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class CacheManager:
    """Filesystem JSON cache keyed by sha256 digests."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, key: CacheKey | str) -> Path:
        """Return the safe JSON path for a cache key."""

        key_text = str(key)
        if not is_sha256_key(key_text):
            raise ValueError("cache key must be a sha256 hex digest")
        return self.root / f"{key_text}.json"

    def put(
        self,
        key: CacheKey,
        value: dict[str, Any],
        metadata: dict[str, Any],
    ) -> CacheEntry:
        """Write a cache entry to disk."""

        entry = CacheEntry(key=key, value=value, metadata=metadata)
        path = self.path_for(key)
        path.write_text(entry.model_dump_json(indent=2), encoding="utf-8")
        return entry

    def get(self, key: CacheKey) -> CacheEntry | None:
        """Read a cache entry from disk if present."""

        path = self.path_for(key)
        if not path.exists():
            return None
        raw = json.loads(path.read_text(encoding="utf-8"))
        return CacheEntry.model_validate(raw)

    def exists(self, key: CacheKey) -> bool:
        """Return whether a cache entry exists."""

        return self.path_for(key).exists()
