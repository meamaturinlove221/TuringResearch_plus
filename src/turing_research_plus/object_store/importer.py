"""Build provider-neutral object artifact indexes and proposed imports."""

from __future__ import annotations

from turing_research_plus.object_store.fake_client import FakeObjectStoreClient
from turing_research_plus.object_store.index import filter_objects_by_patterns
from turing_research_plus.object_store.models import (
    ObjectArtifactIndex,
    ObjectArtifactIndexRequest,
    ObjectArtifactRef,
    ObjectArtifactStatus,
)
from turing_research_plus.object_store.safety import (
    omitted_reason_for_object,
    safety_warnings_for_object_key,
    status_for_object_warnings,
)


def build_object_artifact_index(
    request: ObjectArtifactIndexRequest,
    *,
    fake_client: FakeObjectStoreClient | None = None,
    objects: list[ObjectArtifactRef] | None = None,
) -> ObjectArtifactIndex:
    """Build an object artifact index without cloud SDK calls."""

    source_objects = objects
    if source_objects is None:
        client = fake_client or FakeObjectStoreClient()
        source_objects = client.list_objects(
            provider=request.provider,
            bucket_or_container=request.bucket_or_container,
            prefix=request.prefix,
        )

    selected_candidates = filter_objects_by_patterns(source_objects, request.selected_patterns)
    indexed_objects: list[ObjectArtifactRef] = []
    proposed_imports: list[dict[str, object]] = []
    size: dict[str, int] = {}
    hashes: dict[str, str] = {}
    content_types: dict[str, str] = {}
    omitted_reason: dict[str, str] = {}
    all_warnings: list[str] = []
    evidence_tags: set[str] = set()

    for item in selected_candidates:
        warnings = safety_warnings_for_object_key(
            item.key,
            size=item.size,
            max_size=request.max_object_size_bytes,
        )
        status = status_for_object_warnings(warnings)
        reason = omitted_reason_for_object(warnings) if warnings else None
        indexed = item.model_copy(
            update={
                "status": status,
                "omitted_reason": reason,
                "safety_warnings": warnings,
            }
        )
        indexed_objects.append(indexed)
        size[indexed.key] = indexed.size
        if indexed.hash:
            hashes[indexed.key] = indexed.hash
        if indexed.content_type:
            content_types[indexed.key] = indexed.content_type
        if reason:
            omitted_reason[indexed.key] = reason
        all_warnings.extend(warnings)
        evidence_tags.update(indexed.evidence_tags)
        if status == ObjectArtifactStatus.SELECTED:
            proposed_imports.append(
                {
                    "key": indexed.key,
                    "status": "requires-human-review",
                    "provider": request.provider,
                    "bucket_or_container": request.bucket_or_container,
                    "hash": indexed.hash,
                }
            )

    return ObjectArtifactIndex(
        provider=request.provider,
        bucket_or_container=request.bucket_or_container,
        prefix=request.prefix,
        objects=indexed_objects,
        size=size,
        hash=hashes,
        content_type=content_types,
        status=ObjectArtifactStatus.INDEXED,
        omitted_reason=omitted_reason,
        evidence_tags=sorted(evidence_tags),
        proposed_imports=proposed_imports,
        safety_warnings=sorted(set(all_warnings)),
        requires_human_review=True,
        human_verified=False,
        limitations=[
            "Object store support is provider-neutral and does not use cloud SDKs.",
            "No credentials are stored or required for fake/default indexing.",
            "Object payloads are not downloaded by default.",
            "Object artifacts are indexed, not human verified.",
        ],
    )
