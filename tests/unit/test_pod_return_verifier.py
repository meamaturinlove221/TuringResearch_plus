from __future__ import annotations

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    PodLifecycleStatus,
    verify_pod_context_return,
)


def _lifecycle() -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx-v1-demo",
        source_machine_label="local-planning-machine",
        target_environment_label="review-pod",
        route_id="route-demo",
    )


def test_return_verifier_passes_complete_structured_output() -> None:
    lifecycle = _lifecycle()
    report = verify_pod_context_return(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_metadata={
            "context_package_id": "ctx-v1-demo",
            "route_id": "route-demo",
            "target_environment_label": "review-pod",
            "return_package_id": "return-demo",
            "sha256_manifest": {"RETURN_MANIFEST.yaml": "abc"},
        },
    )

    assert report.status == PodLifecycleStatus.PASS
    assert report.release_blocker is False
    assert report.proposed_updates_only is True


def test_return_verifier_blocks_missing_manifest_and_metadata() -> None:
    report = verify_pod_context_return(_lifecycle(), ["RUN_STATUS.json"], return_metadata={})

    assert report.status == PodLifecycleStatus.BLOCKED
    assert "RETURN_MANIFEST.yaml" in report.missing_return_files
    assert "context_package_id" in report.missing_metadata_fields


def test_return_verifier_blocks_metadata_mismatch() -> None:
    lifecycle = _lifecycle()
    report = verify_pod_context_return(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_metadata={
            "context_package_id": "wrong",
            "route_id": "route-demo",
            "target_environment_label": "review-pod",
            "return_package_id": "return-demo",
            "sha256_manifest": {},
        },
    )

    assert report.status == PodLifecycleStatus.BLOCKED
    assert "return-metadata-mismatch" in {finding.finding_id for finding in report.findings}
