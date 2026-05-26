from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.pod_lifecycle import (
    PodContextLifecycle,
    PodMemoryPolicy,
    PodReturnVerification,
    PodTransferPolicy,
)


def test_pod_context_lifecycle_has_required_review_boundaries() -> None:
    lifecycle = PodContextLifecycle(
        context_package_id="ctx-v1-demo",
        source_machine_label="local-planning-machine",
        target_environment_label="review-pod",
        route_id="route-demo",
    )

    assert lifecycle.requires_human_review is True
    assert lifecycle.memory_policy.bidirectional_memory_sync is False
    assert lifecycle.transfer_policy.remote_execution_allowed is False
    assert lifecycle.return_verification.auto_apply_evidence_updates is False
    assert "PROJECT_CONTEXT.md" in lifecycle.memory_policy.durable_context_files
    assert "RETURN_MANIFEST.yaml" in lifecycle.structured_output_requirements
    assert ".env" in lifecycle.forbidden_files
    assert "local_project_links.yaml" in lifecycle.forbidden_files


def test_memory_policy_rejects_bidirectional_sync() -> None:
    with pytest.raises(ValidationError):
        PodMemoryPolicy(bidirectional_memory_sync=True)


def test_transfer_policy_rejects_execution_flags() -> None:
    with pytest.raises(ValidationError):
        PodTransferPolicy(remote_execution_allowed=True)

    with pytest.raises(ValidationError):
        PodTransferPolicy(git_push_allowed=True)


def test_return_verification_rejects_auto_apply() -> None:
    with pytest.raises(ValidationError):
        PodReturnVerification(auto_apply_evidence_updates=True)
