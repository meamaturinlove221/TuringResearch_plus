"""Context index persistence."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from tuling_research_plus.context.models import ContextIndex, ContextIndexEntry


def index_path(root: str | Path) -> Path:
    """Return the context index path."""

    return Path(root) / "context_index.json"


def load_index(root: str | Path) -> ContextIndex:
    """Load context index or return an empty index."""

    path = index_path(root)
    if not path.exists():
        return ContextIndex()
    raw = json.loads(path.read_text(encoding="utf-8"))
    return ContextIndex.model_validate(raw)


def save_index(root: str | Path, index: ContextIndex) -> Path:
    """Save context index."""

    path = index_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(index.model_dump_json(indent=2), encoding="utf-8")
    return path


def upsert_index_entry(root: str | Path, entry: ContextIndexEntry) -> ContextIndex:
    """Upsert a context index entry."""

    index = load_index(root)
    entries = [
        existing
        for existing in index.entries
        if not (existing.campaign_id == entry.campaign_id and existing.run_id == entry.run_id)
    ]
    entry.updated_at = datetime.now(UTC)
    entries.append(entry)
    index.entries = entries
    save_index(root, index)
    return index
