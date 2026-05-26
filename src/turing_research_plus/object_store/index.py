"""Object artifact index loading and filtering."""

from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.object_store.models import (
    ObjectArtifactIndex,
    ObjectArtifactRef,
    ObjectStoreProvider,
)


def load_object_artifact_index(path: Path) -> ObjectArtifactIndex:
    """Load a provider-neutral object artifact index fixture."""

    payload = json.loads(path.read_text(encoding="utf-8"))
    objects = [ObjectArtifactRef(**item) for item in payload.get("objects", [])]
    return ObjectArtifactIndex(
        provider=ObjectStoreProvider(payload.get("provider", ObjectStoreProvider.GENERIC)),
        bucket_or_container=payload["bucket_or_container"],
        prefix=payload.get("prefix", ""),
        objects=objects,
        evidence_tags=payload.get("evidence_tags", []),
        requires_human_review=payload.get("requires_human_review", True),
    )


def filter_objects_by_patterns(
    objects: list[ObjectArtifactRef],
    selected_patterns: list[str],
) -> list[ObjectArtifactRef]:
    """Filter object refs by substring patterns."""

    if not selected_patterns:
        return objects
    return [
        item
        for item in objects
        if any(pattern in item.key for pattern in selected_patterns)
    ]
