"""Default extension permission policy."""

from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionPermission,
    ExtensionRiskLevel,
    ExtensionSafetyStatus,
    PermissionDecision,
)

FORBIDDEN_PERMISSIONS = {
    ExtensionPermission.EXECUTE_CODE,
    ExtensionPermission.REMOTE_WRITE,
}

RESTRICTED_PERMISSIONS = {
    ExtensionPermission.WRITE_LOCAL_FILES,
    ExtensionPermission.NETWORK_ACCESS,
    ExtensionPermission.LIVE_API,
    ExtensionPermission.REMOTE_READ,
    ExtensionPermission.EXPORT_ARTIFACTS,
    ExtensionPermission.PACKAGE_RELEASE,
}


def evaluate_permission(permission: ExtensionPermission) -> PermissionDecision:
    """Evaluate one permission under the default extension safety policy."""

    if permission in FORBIDDEN_PERMISSIONS:
        return PermissionDecision(
            permission=permission,
            allowed=False,
            status=ExtensionSafetyStatus.FORBIDDEN,
            risk_level=ExtensionRiskLevel.CRITICAL,
            reason=f"{permission.value} is forbidden by default",
        )
    if permission in RESTRICTED_PERMISSIONS:
        return PermissionDecision(
            permission=permission,
            allowed=False,
            status=ExtensionSafetyStatus.RESTRICTED,
            risk_level=ExtensionRiskLevel.HIGH,
            reason=f"{permission.value} requires explicit human approval",
        )
    return PermissionDecision(
        permission=permission,
        allowed=True,
        status=ExtensionSafetyStatus.ALLOW_WITH_REVIEW,
        risk_level=ExtensionRiskLevel.LOW,
        reason=f"{permission.value} is allowed with review",
    )


def evaluate_permissions(permissions: list[ExtensionPermission]) -> list[PermissionDecision]:
    """Evaluate a permission list."""

    return [evaluate_permission(permission) for permission in permissions]
