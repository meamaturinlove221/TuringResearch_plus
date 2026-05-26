from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionPermission,
    ExtensionSafetyStatus,
)
from turing_research_plus.extension_safety.permission_policy import evaluate_permission


def test_read_local_files_allowed_with_review() -> None:
    decision = evaluate_permission(ExtensionPermission.READ_LOCAL_FILES)

    assert decision.allowed is True
    assert decision.status == ExtensionSafetyStatus.ALLOW_WITH_REVIEW


def test_execute_code_forbidden_by_default() -> None:
    decision = evaluate_permission(ExtensionPermission.EXECUTE_CODE)

    assert decision.allowed is False
    assert decision.status == ExtensionSafetyStatus.FORBIDDEN


def test_network_access_is_restricted_not_implicitly_allowed() -> None:
    decision = evaluate_permission(ExtensionPermission.NETWORK_ACCESS)

    assert decision.allowed is False
    assert decision.status == ExtensionSafetyStatus.RESTRICTED


def test_remote_write_forbidden_by_default() -> None:
    decision = evaluate_permission(ExtensionPermission.REMOTE_WRITE)

    assert decision.allowed is False
    assert decision.status == ExtensionSafetyStatus.FORBIDDEN
