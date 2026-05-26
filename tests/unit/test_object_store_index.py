from __future__ import annotations

from pathlib import Path

from turing_research_plus.object_store.index import (
    filter_objects_by_patterns,
    load_object_artifact_index,
)
from turing_research_plus.object_store.models import ObjectStoreProvider

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "object_store_fixture"
    / "artifact_index.json"
)


def test_load_object_artifact_index_fixture() -> None:
    index = load_object_artifact_index(FIXTURE)

    assert index.provider == ObjectStoreProvider.GENERIC
    assert index.bucket_or_container == "vggt-review-artifacts"
    assert any(item.key.endswith("review/failure_report.md") for item in index.objects)


def test_filter_objects_by_patterns() -> None:
    index = load_object_artifact_index(FIXTURE)

    filtered = filter_objects_by_patterns(index.objects, ["review/"])

    assert filtered
    assert all("review/" in item.key for item in filtered)
