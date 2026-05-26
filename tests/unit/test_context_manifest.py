from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.context_manifest import (
    ContextPackBuildStatus,
    ContextPackManifest,
    ContextPackManifestFile,
    render_context_pack_manifest_markdown,
    render_handoff_manifest,
)


def _file(path: str) -> ContextPackManifestFile:
    return ContextPackManifestFile(
        path=path,
        sha256="a" * 64,
        role="durable_context",
    )


def test_context_manifest_reports_missing_required_files() -> None:
    manifest = ContextPackManifest(
        package_id="ctx-demo",
        route_id="route-demo",
        status=ContextPackBuildStatus.BUILT,
        output_dir="out",
        files=[_file("PROJECT_CONTEXT.md")],
    )

    assert "MEMORY.md" in manifest.missing_required_files
    assert manifest.release_blocker is True


def test_context_manifest_rejects_remote_execution_or_raw_data_flags() -> None:
    with pytest.raises(ValidationError):
        ContextPackManifest(
            package_id="ctx-demo",
            route_id="route-demo",
            status=ContextPackBuildStatus.BUILT,
            output_dir="out",
            remote_execution_allowed=True,
        )

    with pytest.raises(ValidationError):
        ContextPackManifest(
            package_id="ctx-demo",
            route_id="route-demo",
            status=ContextPackBuildStatus.BUILT,
            output_dir="out",
            contains_raw_data=True,
        )


def test_render_handoff_manifest_keeps_review_only_boundaries() -> None:
    manifest = ContextPackManifest(
        package_id="ctx-demo",
        route_id="route-demo",
        status=ContextPackBuildStatus.BUILT,
        output_dir="out",
        files=[_file("PROJECT_CONTEXT.md")],
    )
    text = render_handoff_manifest(manifest)

    assert "remote_execution_allowed: false" in text
    assert "live_network_allowed: false" in text
    assert "requires_human_review: true" in text


def test_render_context_pack_manifest_markdown_lists_files() -> None:
    manifest = ContextPackManifest(
        package_id="ctx-demo",
        route_id="route-demo",
        status=ContextPackBuildStatus.BUILT,
        output_dir="out",
        files=[_file("PROJECT_CONTEXT.md")],
    )
    text = render_context_pack_manifest_markdown(manifest)

    assert "# Context Pack Manifest: ctx-demo" in text
    assert "`PROJECT_CONTEXT.md`" in text
