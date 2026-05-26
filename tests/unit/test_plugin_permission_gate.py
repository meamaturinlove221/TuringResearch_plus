from __future__ import annotations

import pytest

from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)


@pytest.mark.parametrize(
    "permission",
    [
        SandboxPermission.EXECUTE_CODE,
        SandboxPermission.SHELL_ACCESS,
        SandboxPermission.SECRETS_ACCESS,
        SandboxPermission.REMOTE_WRITE,
    ],
)
def test_denied_permissions_are_release_blockers(permission: SandboxPermission) -> None:
    decision = evaluate_sandbox_permission(permission)

    assert decision.status == SandboxDecisionStatus.DENIED
    assert decision.allowed is False
    assert decision.release_blocker is True
    assert decision.future_sandbox_requirement is True


def test_network_access_is_explicit_only() -> None:
    decision = evaluate_sandbox_permission(SandboxPermission.NETWORK_ACCESS)

    assert decision.status == SandboxDecisionStatus.EXPLICIT_ONLY
    assert decision.allowed is False
    assert decision.release_blocker is True

    enabled = evaluate_sandbox_permission(
        SandboxPermission.NETWORK_ACCESS,
        explicit_enable=True,
    )
    assert enabled.allowed is True
    assert enabled.requires_explicit_enable is True
    assert enabled.future_sandbox_requirement is True


def test_read_project_files_is_scoped_only() -> None:
    decision = evaluate_sandbox_permission(SandboxPermission.READ_PROJECT_FILES)

    assert decision.status == SandboxDecisionStatus.SCOPED_ONLY
    assert decision.allowed is False
    assert decision.release_blocker is True

    scoped = evaluate_sandbox_permission(
        SandboxPermission.READ_PROJECT_FILES,
        scoped=True,
    )
    assert scoped.allowed is True
    assert scoped.release_blocker is False
