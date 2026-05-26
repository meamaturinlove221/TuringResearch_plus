from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    SessionContextPackManifest,
    build_session_context_pack_manifest,
    render_session_context_pack_manifest,
)


def _lifecycle() -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx-session-parity-demo",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id="route-session-parity",
    )


def test_session_context_pack_manifest_requires_review_only_boundaries() -> None:
    manifest = build_session_context_pack_manifest(
        _lifecycle(),
        ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml", "HARD_GATES.md"],
    )

    assert manifest.memory_bidirectional_sync is False
    assert manifest.proposed_updates_only is True
    assert manifest.requires_human_review is True
    assert manifest.remote_execution_allowed is False
    assert manifest.automatic_git_push_allowed is False
    assert manifest.release_blocker is False
    assert manifest.missing_required_files == []


def test_session_context_pack_manifest_reports_missing_required_files() -> None:
    manifest = build_session_context_pack_manifest(_lifecycle(), ["PROJECT_CONTEXT.md"])

    assert manifest.release_blocker is True
    assert manifest.missing_required_files == ["MEMORY.md", "ROUTE_SPEC.yaml"]


def test_session_context_pack_manifest_omits_unsafe_files() -> None:
    manifest = build_session_context_pack_manifest(
        _lifecycle(),
        ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml", ".env", "../secret.txt"],
    )

    omitted = {item.path for item in manifest.files if item.omitted}
    assert ".env" in omitted
    assert "../secret.txt" in omitted
    assert manifest.archive_safety.release_blocker is True


def test_session_context_pack_manifest_rejects_bidirectional_sync() -> None:
    with pytest.raises(ValidationError):
        SessionContextPackManifest(
            context_package_id="ctx",
            route_id="route",
            source_machine_label="local",
            target_environment_label="pod",
            memory_bidirectional_sync=True,
        )


def test_render_session_context_pack_manifest_is_deterministic() -> None:
    manifest = build_session_context_pack_manifest(
        _lifecycle(),
        ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"],
    )
    rendered = render_session_context_pack_manifest(manifest)

    assert "context_package_id: ctx-session-parity-demo" in rendered
    assert "memory_bidirectional_sync: false" in rendered
    assert "release_blocker: false" in rendered
