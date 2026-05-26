from __future__ import annotations

from turing_research_plus.object_store.fake_client import FakeObjectStoreClient
from turing_research_plus.object_store.models import ObjectStoreProvider


def test_fake_object_store_client_returns_vggt_shaped_metadata() -> None:
    client = FakeObjectStoreClient()

    objects = client.list_objects(
        provider=ObjectStoreProvider.GENERIC,
        bucket_or_container="vggt-review-artifacts",
        prefix="modal-sparseconv-review",
    )

    assert any(item.key.endswith("review/final_status.json") for item in objects)
    assert any(item.key.endswith("large/predictions.npz") for item in objects)
    assert any(item.key.endswith("private/SMPLX_model.pkl") for item in objects)
