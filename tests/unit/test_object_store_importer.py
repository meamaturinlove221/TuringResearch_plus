from __future__ import annotations

from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.models import (
    ObjectArtifactIndexRequest,
    ObjectArtifactStatus,
    ObjectStoreProvider,
)


def test_object_store_importer_builds_fake_index_without_cloud_sdk() -> None:
    index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            provider=ObjectStoreProvider.GENERIC,
            bucket_or_container="vggt-review-artifacts",
            prefix="modal-sparseconv-review",
        )
    )

    assert any(item.key.endswith("review/final_status.json") for item in index.objects)
    assert any(item.status == ObjectArtifactStatus.SELECTED for item in index.objects)
    assert any(item.status == ObjectArtifactStatus.LARGE_METADATA_ONLY for item in index.objects)
    assert any(item.status == ObjectArtifactStatus.UNSAFE for item in index.objects)
    assert index.proposed_imports
    assert all(item["status"] == "requires-human-review" for item in index.proposed_imports)
    assert index.human_verified is False


def test_object_store_importer_filters_selected_patterns() -> None:
    index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            provider=ObjectStoreProvider.GENERIC,
            bucket_or_container="vggt-review-artifacts",
            prefix="modal-sparseconv-review",
            selected_patterns=["review/"],
        )
    )

    assert index.objects
    assert all("review/" in item.key for item in index.objects)
