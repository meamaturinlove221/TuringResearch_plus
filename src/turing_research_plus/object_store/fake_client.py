"""Fake provider-neutral object store client."""

from __future__ import annotations

from turing_research_plus.object_store.models import (
    ObjectArtifactRef,
    ObjectStoreProvider,
)


class FakeObjectStoreClient:
    """Fake object store listing client.

    It never contacts S3, R2, OSS, GCS, or any cloud provider.
    """

    def list_objects(
        self,
        *,
        provider: ObjectStoreProvider,
        bucket_or_container: str,
        prefix: str = "",
    ) -> list[ObjectArtifactRef]:
        """Return VGGT-shaped object metadata."""

        base = prefix.strip("/")
        prefix_part = f"{base}/" if base else ""
        return [
            ObjectArtifactRef(
                key=f"{prefix_part}review/final_status.json",
                size=512,
                hash="a" * 64,
                content_type="application/json",
                evidence_tags=["run-status", "review"],
            ),
            ObjectArtifactRef(
                key=f"{prefix_part}review/failure_report.md",
                size=2048,
                hash="b" * 64,
                content_type="text/markdown",
                evidence_tags=["failure", "review"],
            ),
            ObjectArtifactRef(
                key=f"{prefix_part}review/artifact_index.md",
                size=1024,
                hash="c" * 64,
                content_type="text/markdown",
                evidence_tags=["artifact-index"],
            ),
            ObjectArtifactRef(
                key=f"{prefix_part}large/predictions.npz",
                size=250_000_000,
                hash="d" * 64,
                content_type="application/octet-stream",
                evidence_tags=["large-array"],
            ),
            ObjectArtifactRef(
                key=f"{prefix_part}private/SMPLX_model.pkl",
                size=100_000_000,
                hash="e" * 64,
                content_type="application/octet-stream",
                evidence_tags=["body-model"],
            ),
            ObjectArtifactRef(
                key=f"{prefix_part}.env",
                size=128,
                hash="f" * 64,
                content_type="text/plain",
                evidence_tags=["unsafe"],
            ),
        ]
