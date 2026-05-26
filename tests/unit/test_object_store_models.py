from __future__ import annotations

import pytest

from turing_research_plus.object_store.models import (
    ObjectArtifactIndex,
    ObjectArtifactRef,
    ObjectArtifactStatus,
    ObjectStoreProvider,
)


def test_object_artifact_index_serializes_and_exports_markdown() -> None:
    index = ObjectArtifactIndex(
        provider=ObjectStoreProvider.GENERIC,
        bucket_or_container="vggt-review-artifacts",
        prefix="modal-sparseconv-review",
        objects=[
            ObjectArtifactRef(
                key="modal-sparseconv-review/review/final_status.json",
                size=512,
                status=ObjectArtifactStatus.SELECTED,
            )
        ],
    )

    payload = index.model_dump(mode="json")
    markdown = index.to_markdown()

    assert payload["requires_human_review"] is True
    assert payload["human_verified"] is False
    assert "final_status.json" in markdown


def test_object_artifact_index_cannot_be_human_verified() -> None:
    with pytest.raises(ValueError, match="indexed, not verified"):
        ObjectArtifactIndex(
            provider=ObjectStoreProvider.GENERIC,
            bucket_or_container="vggt-review-artifacts",
            human_verified=True,
        )
