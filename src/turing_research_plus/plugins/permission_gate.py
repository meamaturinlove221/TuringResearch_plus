"""Permission gate for plugin sandbox policy."""

from __future__ import annotations

from turing_research_plus.plugins.sandbox_policy import (
    PluginSandboxPolicy,
    SandboxDecisionStatus,
    SandboxPermission,
    SandboxPermissionDecision,
    SandboxRiskLevel,
    default_plugin_sandbox_policy,
)


def evaluate_sandbox_permission(
    permission: SandboxPermission,
    *,
    explicit_enable: bool = False,
    scoped: bool = False,
    policy: PluginSandboxPolicy | None = None,
) -> SandboxPermissionDecision:
    """Evaluate one permission against the sandbox policy."""

    active_policy = default_plugin_sandbox_policy() if policy is None else policy

    if permission in active_policy.denied_permissions:
        return SandboxPermissionDecision(
            permission=permission,
            status=SandboxDecisionStatus.DENIED,
            allowed=False,
            requires_explicit_enable=True,
            release_blocker=True,
            future_sandbox_requirement=True,
            risk_level=SandboxRiskLevel.CRITICAL,
            reason=f"{permission.value} is denied by default",
        )

    if permission in active_policy.scoped_permissions:
        return SandboxPermissionDecision(
            permission=permission,
            status=SandboxDecisionStatus.SCOPED_ONLY,
            allowed=scoped,
            requires_explicit_enable=not scoped,
            release_blocker=not scoped,
            future_sandbox_requirement=False,
            risk_level=SandboxRiskLevel.LOW if scoped else SandboxRiskLevel.HIGH,
            reason=(
                f"{permission.value} is allowed only with scoped project paths"
                if scoped
                else f"{permission.value} requires scoped project paths"
            ),
        )

    if permission in active_policy.explicit_permissions:
        return SandboxPermissionDecision(
            permission=permission,
            status=SandboxDecisionStatus.EXPLICIT_ONLY,
            allowed=explicit_enable,
            requires_explicit_enable=True,
            release_blocker=not explicit_enable,
            future_sandbox_requirement=permission
            in {
                SandboxPermission.NETWORK_ACCESS,
                SandboxPermission.LIVE_API_ACCESS,
                SandboxPermission.REMOTE_READ,
                SandboxPermission.ARTIFACT_EXPORT,
                SandboxPermission.WRITE_PROJECT_FILES,
            },
            risk_level=SandboxRiskLevel.MEDIUM if explicit_enable else SandboxRiskLevel.HIGH,
            reason=(
                f"{permission.value} allowed only because explicit enable is set"
                if explicit_enable
                else f"{permission.value} requires explicit enable"
            ),
        )

    return SandboxPermissionDecision(
        permission=permission,
        status=SandboxDecisionStatus.DENIED,
        allowed=False,
        requires_explicit_enable=True,
        release_blocker=True,
        future_sandbox_requirement=True,
        risk_level=SandboxRiskLevel.HIGH,
        reason=f"{permission.value} is not recognized as an allowed permission",
    )


def evaluate_sandbox_permissions(
    permissions: list[SandboxPermission],
    *,
    explicit_enable: bool = False,
    scoped: bool = False,
    policy: PluginSandboxPolicy | None = None,
) -> list[SandboxPermissionDecision]:
    """Evaluate a list of sandbox permissions."""

    return [
        evaluate_sandbox_permission(
            permission,
            explicit_enable=explicit_enable,
            scoped=scoped,
            policy=policy,
        )
        for permission in permissions
    ]
