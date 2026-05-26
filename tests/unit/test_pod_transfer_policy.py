from __future__ import annotations

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    PodLifecycleStatus,
    transfer_warnings_for_path,
    validate_transfer_policy,
)


def test_transfer_warnings_block_dotfiles_and_traversal() -> None:
    assert "forbidden-dotfile" in transfer_warnings_for_path(".env")
    assert "unsafe-archive-path-traversal" in transfer_warnings_for_path("../secrets.txt")
    assert "shell-metacharacter-risk" in transfer_warnings_for_path("safe;rm.txt")


def test_transfer_warnings_block_body_models_and_huge_npz() -> None:
    warnings = transfer_warnings_for_path("models/SMPLX_NEUTRAL.npz", file_size=10)
    assert "forbidden-body-model-file" in warnings

    warnings = transfer_warnings_for_path("arrays/review.npz", file_size=9_000_000)
    assert "huge-npz-forbidden" in warnings


def test_validate_transfer_policy_blocks_shell_risk_in_identifiers() -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx;bad",
        source_machine_label="local",
        target_environment_label="review-pod",
        route_id="route-demo",
    )
    report = validate_transfer_policy(lifecycle)

    assert report.status == PodLifecycleStatus.BLOCKED
    assert "shell-metacharacter-risk" in {finding.finding_id for finding in report.findings}
