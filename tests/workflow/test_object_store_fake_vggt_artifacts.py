from __future__ import annotations

from pathlib import Path

from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.index import load_object_artifact_index
from turing_research_plus.object_store.models import (
    ObjectArtifactIndexRequest,
    ObjectArtifactStatus,
)

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "object_store_fixture"
    / "artifact_index.json"
)


def test_object_store_fake_vggt_artifacts_preserve_boundaries() -> None:
    fixture_index = load_object_artifact_index(FIXTURE)
    index = build_object_artifact_index(
        ObjectArtifactIndexRequest(
            provider=fixture_index.provider,
            bucket_or_container=fixture_index.bucket_or_container,
            prefix=fixture_index.prefix,
            selected_patterns=["review/", "large/", "private/", ".env"],
        ),
        objects=fixture_index.objects,
    )
    markdown = index.to_markdown()

    assert any(item.key.endswith("review/final_status.json") for item in index.objects)
    assert any(item.key.endswith("large/predictions.npz") for item in index.objects)
    assert any(item.status == ObjectArtifactStatus.LARGE_METADATA_ONLY for item in index.objects)
    assert any(item.key.endswith("private/SMPLX_model.pkl") for item in index.objects)
    assert any(item.status == ObjectArtifactStatus.UNSAFE for item in index.objects)
    assert all(item["status"] == "requires-human-review" for item in index.proposed_imports)
    assert index.requires_human_review is True
    assert index.human_verified is False
    assert "SparseConv3D" not in markdown
