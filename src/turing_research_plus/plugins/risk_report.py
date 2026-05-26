"""Risk report for plugin sandbox policy checks."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permissions
from turing_research_plus.plugins.sandbox_policy import (
    PluginSandboxPolicy,
    SandboxPermission,
    SandboxPermissionDecision,
    SandboxRiskLevel,
    default_plugin_sandbox_policy,
)


class PluginSandboxRiskReport(BaseModel):
    """Review report for plugin sandbox policy decisions."""

    model_config = ConfigDict(extra="forbid")

    plugin_id: str = Field(min_length=1)
    requested_permissions: list[SandboxPermission] = Field(default_factory=list)
    decisions: list[SandboxPermissionDecision] = Field(default_factory=list)
    severity: SandboxRiskLevel
    allowed_permissions: list[SandboxPermission] = Field(default_factory=list)
    denied_permissions: list[SandboxPermission] = Field(default_factory=list)
    requires_explicit_enable: list[SandboxPermission] = Field(default_factory=list)
    release_blocker: bool = False
    future_sandbox_requirements: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    implements_os_sandbox: bool = False

    @model_validator(mode="after")
    def report_is_policy_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("plugin sandbox reports require human review")
        if self.implements_os_sandbox:
            raise ValueError("plugin sandbox report must not claim OS sandbox implementation")
        return self


def build_plugin_sandbox_report(
    plugin_id: str,
    requested_permissions: list[SandboxPermission],
    *,
    explicit_enable: bool = False,
    scoped: bool = False,
    policy: PluginSandboxPolicy | None = None,
) -> PluginSandboxRiskReport:
    """Build a sandbox policy report for one plugin."""

    active_policy = default_plugin_sandbox_policy() if policy is None else policy
    decisions = evaluate_sandbox_permissions(
        requested_permissions,
        explicit_enable=explicit_enable,
        scoped=scoped,
        policy=active_policy,
    )
    release_blocker = any(decision.release_blocker for decision in decisions)
    denied = [decision.permission for decision in decisions if not decision.allowed]
    allowed = [decision.permission for decision in decisions if decision.allowed]
    explicit = [
        decision.permission for decision in decisions if decision.requires_explicit_enable
    ]
    future = [
        f"{decision.permission.value}: {decision.reason}"
        for decision in decisions
        if decision.future_sandbox_requirement
    ]
    severity = _max_risk(decision.risk_level for decision in decisions)

    return PluginSandboxRiskReport(
        plugin_id=plugin_id,
        requested_permissions=requested_permissions,
        decisions=decisions,
        severity=severity,
        allowed_permissions=allowed,
        denied_permissions=denied,
        requires_explicit_enable=explicit,
        release_blocker=release_blocker,
        future_sandbox_requirements=future,
    )


def _max_risk(levels: Iterable[SandboxRiskLevel]) -> SandboxRiskLevel:
    order = {
        SandboxRiskLevel.LOW: 0,
        SandboxRiskLevel.MEDIUM: 1,
        SandboxRiskLevel.HIGH: 2,
        SandboxRiskLevel.CRITICAL: 3,
    }
    highest = SandboxRiskLevel.LOW
    for level in levels:
        if order[level] > order[highest]:
            highest = level
    return highest
