from __future__ import annotations

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    PodLifecycleStatus,
    run_pod_context_preflight,
)


def _lifecycle() -> PodContextLifecycle:
    return PodContextLifecycle(
        context_package_id="ctx-v1-demo",
        source_machine_label="local-planning-machine",
        target_environment_label="review-pod",
        route_id="route-demo",
    )


def test_preflight_passes_safe_context_package_paths() -> None:
    report = run_pod_context_preflight(
        _lifecycle(),
        candidate_paths=[
            "PROJECT_CONTEXT.md",
            "MEMORY.md",
            "ROUTE_SPEC.yaml",
            "RETURN_MANIFEST.yaml",
        ],
    )

    assert report.status == PodLifecycleStatus.PASS
    assert report.release_blocker is False
    assert report.requires_human_review is True


def test_preflight_blocks_secrets_and_local_project_links() -> None:
    report = run_pod_context_preflight(
        _lifecycle(),
        candidate_paths=["PROJECT_CONTEXT.md", "local_project_links.yaml"],
        context_text="API_KEY=notarealbutlongsecret",
    )

    finding_ids = {finding.finding_id for finding in report.findings}
    assert report.status == PodLifecycleStatus.BLOCKED
    assert "forbidden-local-project-links" in finding_ids
    assert "possible-secret-value" in finding_ids


def test_preflight_warns_when_durable_context_files_missing() -> None:
    report = run_pod_context_preflight(_lifecycle(), candidate_paths=["PROJECT_CONTEXT.md"])

    assert report.status == PodLifecycleStatus.PASS_WITH_WARNINGS
    assert "missing-durable-context-file" in {finding.finding_id for finding in report.findings}
