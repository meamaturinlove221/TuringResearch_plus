"""Local tool wrappers for cloud object artifact indexing."""

from __future__ import annotations

from turing_research_plus.object_store.importer import build_object_artifact_index
from turing_research_plus.object_store.models import (
    ObjectArtifactIndex,
    ObjectArtifactIndexRequest,
)


def artifact_cloud_index_optional(request: ObjectArtifactIndexRequest) -> ObjectArtifactIndex:
    """Build a provider-neutral object artifact index."""

    return build_object_artifact_index(request)
