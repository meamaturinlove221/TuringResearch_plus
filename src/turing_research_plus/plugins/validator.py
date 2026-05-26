"""Validate plugin manifests without executing plugin code."""

from __future__ import annotations

from pydantic import ValidationError

from turing_research_plus.plugins.models import (
    PluginManifest,
    PluginSafetyLevel,
    PluginStatus,
    PluginValidationIssue,
    PluginValidationReport,
)


def validate_plugin_manifest(payload: dict[str, object] | PluginManifest) -> PluginValidationReport:
    """Validate a plugin manifest and return a review report."""

    try:
        manifest = payload if isinstance(payload, PluginManifest) else PluginManifest(**payload)
    except ValidationError as exc:
        plugin_id = (
            str(payload.get("plugin_id", "unknown"))
            if isinstance(payload, dict)
            else "unknown"
        )
        return PluginValidationReport(
            plugin_id=plugin_id,
            valid=False,
            issues=[
                PluginValidationIssue(
                    severity="high",
                    message=str(error["msg"]),
                    field=".".join(str(item) for item in error["loc"]),
                )
                for error in exc.errors()
            ],
            safety_level=PluginSafetyLevel.DISABLED,
            status=PluginStatus.DISABLED,
        )

    issues: list[PluginValidationIssue] = []
    if manifest.third_party and manifest.status != PluginStatus.DISABLED:
        issues.append(
            PluginValidationIssue(
                severity="high",
                field="status",
                message="third-party plugins must be disabled by default",
            )
        )
    if not manifest.required_permissions:
        issues.append(
            PluginValidationIssue(
                severity="high",
                field="required_permissions",
                message="plugin manifest must declare permissions",
            )
        )
    if manifest.executes_code:
        issues.append(
            PluginValidationIssue(
                severity="critical",
                field="executes_code",
                message="plugin validation never executes plugin code",
            )
        )
    if manifest.python_entrypoint:
        issues.append(
            PluginValidationIssue(
                severity="critical",
                field="python_entrypoint",
                message="unknown Python entrypoints are not loaded",
            )
        )

    return PluginValidationReport(
        plugin_id=manifest.plugin_id,
        valid=not issues,
        issues=issues,
        safety_level=manifest.safety_level,
        status=manifest.status,
        executes_code=False,
        loads_entrypoint=False,
        requires_human_review=True,
    )
