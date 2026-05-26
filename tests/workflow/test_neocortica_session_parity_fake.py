from __future__ import annotations

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    PodLifecycleStatus,
    build_platform_compatibility_report,
    build_session_context_pack_manifest,
    build_structured_return_manifest,
    run_pod_context_preflight,
    validate_context_archive_entries,
    verify_pod_context_return,
)


def test_neocortica_session_parity_fake_flow_is_review_only() -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx-session-parity-demo",
        source_machine_label="local-review-machine",
        target_environment_label="linux-review-pod",
        route_id="route-session-parity",
    )
    context_files = ["PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"]

    pack = build_session_context_pack_manifest(lifecycle, context_files)
    archive = validate_context_archive_entries(context_files)
    platform = build_platform_compatibility_report(
        source_platform="Windows",
        target_platform="Linux pod",
    )
    preflight = run_pod_context_preflight(lifecycle, candidate_paths=context_files)
    returned = build_structured_return_manifest(
        lifecycle,
        lifecycle.return_verification.required_files,
        return_package_id="return-session-parity-demo",
    )
    verification = verify_pod_context_return(
        lifecycle,
        [item.path for item in returned.files if item.status == "present"],
        return_metadata=returned.to_metadata(),
    )

    assert pack.release_blocker is False
    assert archive.release_blocker is False
    assert "windows-to-linux-unpack-requires-path-validation" in platform.warnings
    assert preflight.status == PodLifecycleStatus.PASS
    assert verification.status == PodLifecycleStatus.PASS
    assert lifecycle.transfer_policy.remote_execution_allowed is False
    assert lifecycle.transfer_policy.git_push_allowed is False
    assert lifecycle.conflict_policy.no_bidirectional_memory_sync is True
