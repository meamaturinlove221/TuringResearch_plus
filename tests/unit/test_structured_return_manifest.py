from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    StructuredReturnManifest,
    build_structured_return_manifest,
    render_structured_return_manifest,
    verify_pod_context_return,
)


def _lifecycle() -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx-session-parity-demo",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id="route-session-parity",
    )


def test_structured_return_manifest_tracks_required_files() -> None:
    lifecycle = _lifecycle()
    manifest = build_structured_return_manifest(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_package_id="return-session-parity-demo",
        sha256_manifest={"RETURN_MANIFEST.yaml": "abc123"},
    )

    assert manifest.auto_apply_evidence_updates is False
    assert manifest.proposed_evidence_updates_only is True
    assert manifest.requires_human_review is True
    assert manifest.missing_required_files == []
    assert manifest.to_metadata()["context_package_id"] == lifecycle.context_package_id


def test_structured_return_manifest_records_missing_files() -> None:
    manifest = build_structured_return_manifest(
        _lifecycle(),
        ["RETURN_MANIFEST.yaml"],
        return_package_id="return-session-parity-demo",
    )

    assert "FINAL_STATUS.json" in manifest.missing_required_files
    assert "SHA256SUMS.txt" in manifest.missing_required_files


def test_structured_return_manifest_rejects_auto_apply() -> None:
    with pytest.raises(ValidationError):
        StructuredReturnManifest(
            return_package_id="return",
            context_package_id="ctx",
            route_id="route",
            target_environment_label="pod",
            auto_apply_evidence_updates=True,
        )


def test_structured_return_manifest_works_with_existing_verifier() -> None:
    lifecycle = _lifecycle()
    manifest = build_structured_return_manifest(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_package_id="return-session-parity-demo",
    )
    report = verify_pod_context_return(
        lifecycle,
        [item.path for item in manifest.files if item.status == "present"],
        return_metadata=manifest.to_metadata(),
    )

    assert report.release_blocker is False


def test_render_structured_return_manifest_is_deterministic() -> None:
    manifest = build_structured_return_manifest(
        _lifecycle(),
        ["RETURN_MANIFEST.yaml"],
        return_package_id="return-session-parity-demo",
    )
    rendered = render_structured_return_manifest(manifest)

    assert "return_package_id: return-session-parity-demo" in rendered
    assert "auto_apply_evidence_updates: false" in rendered
    assert "requires_human_review: true" in rendered
