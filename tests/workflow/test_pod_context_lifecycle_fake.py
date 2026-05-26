from __future__ import annotations

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    PodLifecycleStatus,
    merge_pod_lifecycle_reports,
    render_pod_lifecycle_safety_report,
    run_pod_context_preflight,
    verify_pod_context_return,
)


def test_pod_context_lifecycle_fake_roundtrip_is_review_only() -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx-v1-upstream-refresh-demo",
        source_machine_label="local-planning-machine",
        target_environment_label="review-pod",
        route_id="route-demo",
    )

    preflight = run_pod_context_preflight(
        lifecycle,
        candidate_paths=[
            "PROJECT_CONTEXT.md",
            "MEMORY.md",
            "ROUTE_SPEC.yaml",
            "RETURN_MANIFEST.yaml",
        ],
    )
    returned = verify_pod_context_return(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_metadata={
            "context_package_id": lifecycle.context_package_id,
            "route_id": lifecycle.route_id,
            "target_environment_label": lifecycle.target_environment_label,
            "return_package_id": "return-demo",
            "sha256_manifest": {"RETURN_MANIFEST.yaml": "abc"},
        },
    )
    merged = merge_pod_lifecycle_reports(preflight, returned)
    markdown = render_pod_lifecycle_safety_report(merged)

    assert merged.status == PodLifecycleStatus.PASS
    assert merged.release_blocker is False
    assert merged.proposed_updates_only is True
    assert "Requires human review: `true`" in markdown
    assert "Missing Return Files" in markdown
