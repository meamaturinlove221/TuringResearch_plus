"""Static plugin compatibility checks.

Compatibility means the declarations line up. It is not a permission grant,
runtime load approval, or safety certification.
"""

from __future__ import annotations

import re
from pathlib import Path

from pydantic import ValidationError

from turing_research_plus.capabilities.models import CapabilityEntry
from turing_research_plus.mcp_plugins.models import MCPPluginRegistry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry
from turing_research_plus.plugins.compat_report import (
    PluginCompatibilityFinding,
    PluginCompatibilityMatrix,
    PluginCompatibilityReport,
    PluginCompatibilitySeverity,
    PluginCompatibilityStatus,
)
from turing_research_plus.plugins.manifest import load_plugin_manifest, load_plugin_manifest_payload
from turing_research_plus.plugins.models import PluginManifest
from turing_research_plus.plugins.risk_report import build_plugin_sandbox_report
from turing_research_plus.plugins.sandbox_policy import SandboxPermission
from turing_research_plus.plugins.validator import validate_plugin_manifest

OLD_PROJECT_NAME = "Tu" + "lingResearch"
CAPABILITY_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
FORBIDDEN_SANDBOX_PERMISSIONS = {
    SandboxPermission.EXECUTE_CODE,
    SandboxPermission.SHELL_ACCESS,
    SandboxPermission.SECRETS_ACCESS,
    SandboxPermission.REMOTE_WRITE,
}
PLUGIN_PERMISSION_TO_SANDBOX = {
    "read_project_files": SandboxPermission.READ_PROJECT_FILES,
    "read_demo_markdown": SandboxPermission.READ_PROJECT_FILES,
    "read_demo_fixture": SandboxPermission.READ_PROJECT_FILES,
    "write_project_files": SandboxPermission.WRITE_PROJECT_FILES,
    "write_demo_export_manifest": SandboxPermission.ARTIFACT_EXPORT,
    "export_artifacts": SandboxPermission.ARTIFACT_EXPORT,
    "network_access": SandboxPermission.NETWORK_ACCESS,
    "live_api": SandboxPermission.LIVE_API_ACCESS,
    "live_api_access": SandboxPermission.LIVE_API_ACCESS,
    "remote_read": SandboxPermission.REMOTE_READ,
    "remote_write": SandboxPermission.REMOTE_WRITE,
    "execute_code": SandboxPermission.EXECUTE_CODE,
    "shell_access": SandboxPermission.SHELL_ACCESS,
    "secrets_access": SandboxPermission.SECRETS_ACCESS,
}


def check_plugin_compatibility(
    manifest_path: Path,
    *,
    mcp_registry: MCPPluginRegistry | None = None,
    capability_entries: list[CapabilityEntry] | None = None,
    docs: list[Path] | None = None,
    tests: list[Path] | None = None,
    scoped_permissions: bool = True,
    explicit_permissions: bool = True,
) -> PluginCompatibilityReport:
    """Check one local plugin manifest for static compatibility."""

    findings: list[PluginCompatibilityFinding] = []
    docs_to_check = docs if docs is not None else _default_docs_for_manifest(manifest_path)
    tests_to_check = tests if tests is not None else []

    manifest, manifest_schema_valid = _load_manifest_with_findings(manifest_path, findings)
    plugin_id = manifest.plugin_id if manifest is not None else manifest_path.parent.name
    capability_ids = (
        [capability.capability_id for capability in manifest.capabilities] if manifest else []
    )

    capability_ids_valid = _check_capability_ids(capability_ids, findings)
    required_permissions_declared = _check_required_permissions(manifest, findings)
    safety_policy_satisfied, no_forbidden_permission = _check_sandbox_policy(
        manifest,
        findings,
        scoped_permissions=scoped_permissions,
        explicit_permissions=explicit_permissions,
    )
    mcp_mapping_valid, no_core_tool_override, mcp_tools = _check_mcp_mapping(
        manifest,
        mcp_registry,
        findings,
    )
    capability_catalog_valid = _check_capability_catalog(manifest, capability_entries, findings)
    docs_present = _check_paths_present("docs.present", docs_to_check, "docs", findings)
    tests_declared = _check_paths_present("tests.declared", tests_to_check, "tests", findings)
    no_old_project_naming = _check_old_project_naming(
        manifest_path,
        docs_to_check,
        findings,
    )
    if not capability_catalog_valid:
        capability_ids_valid = False

    matrix = PluginCompatibilityMatrix(
        manifest_schema_valid=manifest_schema_valid,
        capability_ids_valid=capability_ids_valid,
        required_permissions_declared=required_permissions_declared,
        safety_policy_satisfied=safety_policy_satisfied,
        mcp_mapping_valid=mcp_mapping_valid,
        docs_present=docs_present,
        tests_declared=tests_declared,
        no_core_tool_override=no_core_tool_override,
        no_old_project_naming=no_old_project_naming,
        no_forbidden_permission=no_forbidden_permission,
    )

    status = _status_from_findings(findings, matrix)
    return PluginCompatibilityReport(
        plugin_id=plugin_id,
        status=status,
        matrix=matrix,
        findings=findings,
        capability_ids=capability_ids,
        mcp_tools=mcp_tools,
        docs=[str(path) for path in docs_to_check],
        tests=[str(path) for path in tests_to_check],
        warnings=[
            "Compatibility is metadata review only.",
            "The report does not enable plugins or execute code.",
        ],
        requires_human_review=True,
        executes_plugin_code=False,
        loads_entrypoint=False,
        starts_mcp_server=False,
        enables_plugin=False,
    )


def _load_manifest_with_findings(
    manifest_path: Path,
    findings: list[PluginCompatibilityFinding],
) -> tuple[PluginManifest | None, bool]:
    try:
        payload = load_plugin_manifest_payload(manifest_path)
        report = validate_plugin_manifest(payload)
        for issue in report.issues:
            findings.append(
                PluginCompatibilityFinding(
                    check_id="manifest.schema",
                    passed=False,
                    severity=PluginCompatibilitySeverity.ERROR,
                    message=issue.message,
                    release_blocker=issue.severity in {"critical", "high"},
                )
            )
        manifest = load_plugin_manifest(manifest_path)
    except (OSError, ValueError, ValidationError) as exc:
        findings.append(
            PluginCompatibilityFinding(
                check_id="manifest.schema",
                passed=False,
                severity=PluginCompatibilitySeverity.BLOCKER,
                message=f"plugin manifest is invalid: {exc}",
                release_blocker=True,
            )
        )
        return None, False

    findings.append(
        PluginCompatibilityFinding(
            check_id="manifest.schema",
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message="plugin manifest schema is valid",
        )
    )
    return manifest, report.valid


def _check_capability_ids(
    capability_ids: list[str],
    findings: list[PluginCompatibilityFinding],
) -> bool:
    invalid = [item for item in capability_ids if not CAPABILITY_ID_PATTERN.match(item)]
    duplicate = len(capability_ids) != len(set(capability_ids))
    if not capability_ids:
        findings.append(
            PluginCompatibilityFinding(
                check_id="capability.ids",
                passed=False,
                severity=PluginCompatibilitySeverity.ERROR,
                message="plugin must declare at least one capability",
                release_blocker=True,
            )
        )
        return False
    if invalid or duplicate:
        findings.append(
            PluginCompatibilityFinding(
                check_id="capability.ids",
                passed=False,
                severity=PluginCompatibilitySeverity.ERROR,
                message=f"invalid or duplicate capability ids: {sorted(set(invalid))}",
                release_blocker=True,
            )
        )
        return False
    findings.append(
        PluginCompatibilityFinding(
            check_id="capability.ids",
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message="capability ids are syntactically valid and unique",
        )
    )
    return True


def _check_required_permissions(
    manifest: PluginManifest | None,
    findings: list[PluginCompatibilityFinding],
) -> bool:
    if manifest is None or not manifest.required_permissions:
        findings.append(
            PluginCompatibilityFinding(
                check_id="permissions.declared",
                passed=False,
                severity=PluginCompatibilitySeverity.ERROR,
                message="required permissions must be declared",
                release_blocker=True,
            )
        )
        return False
    findings.append(
        PluginCompatibilityFinding(
            check_id="permissions.declared",
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message="required permissions are declared",
        )
    )
    return True


def _check_sandbox_policy(
    manifest: PluginManifest | None,
    findings: list[PluginCompatibilityFinding],
    *,
    scoped_permissions: bool,
    explicit_permissions: bool,
) -> tuple[bool, bool]:
    if manifest is None:
        return False, False

    sandbox_permissions = _sandbox_permissions_for_manifest(manifest)
    forbidden = sorted(
        {
            permission.value
            for permission in sandbox_permissions
            if permission in FORBIDDEN_SANDBOX_PERMISSIONS
        }
    )
    if forbidden:
        findings.append(
            PluginCompatibilityFinding(
                check_id="permissions.forbidden",
                passed=False,
                severity=PluginCompatibilitySeverity.BLOCKER,
                message=f"forbidden permissions requested: {forbidden}",
                release_blocker=True,
            )
        )
        no_forbidden_permission = False
    else:
        findings.append(
            PluginCompatibilityFinding(
                check_id="permissions.forbidden",
                passed=True,
                severity=PluginCompatibilitySeverity.INFO,
                message="no forbidden sandbox permission is requested",
            )
        )
        no_forbidden_permission = True

    sandbox_report = build_plugin_sandbox_report(
        manifest.plugin_id,
        sandbox_permissions,
        explicit_enable=explicit_permissions,
        scoped=scoped_permissions,
    )
    if sandbox_report.release_blocker:
        findings.append(
            PluginCompatibilityFinding(
                check_id="safety.policy",
                passed=False,
                severity=PluginCompatibilitySeverity.ERROR,
                message="sandbox policy has release blockers",
                release_blocker=True,
            )
        )
        return False, no_forbidden_permission

    findings.append(
        PluginCompatibilityFinding(
            check_id="safety.policy",
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message="sandbox policy is satisfied for declared compatibility review",
        )
    )
    return True, no_forbidden_permission


def _check_mcp_mapping(
    manifest: PluginManifest | None,
    registry: MCPPluginRegistry | None,
    findings: list[PluginCompatibilityFinding],
) -> tuple[bool, bool, list[str]]:
    if manifest is None:
        return False, False, []
    if registry is None:
        findings.append(
            PluginCompatibilityFinding(
                check_id="mcp.mapping",
                passed=False,
                severity=PluginCompatibilitySeverity.WARNING,
                message="no MCP mapping was supplied",
            )
        )
        findings.append(
            PluginCompatibilityFinding(
                check_id="mcp.no_core_override",
                passed=True,
                severity=PluginCompatibilitySeverity.INFO,
                message="no supplied MCP mapping overrides core tools",
            )
        )
        return False, True, []

    matching = [entry for entry in registry.entries if entry.plugin_id == manifest.plugin_id]
    validation = validate_mcp_plugin_registry(
        MCPPluginRegistry(registry_id=registry.registry_id, entries=matching)
    )
    for issue in validation.issues:
        findings.append(
            PluginCompatibilityFinding(
                check_id="mcp.mapping",
                passed=False,
                severity=PluginCompatibilitySeverity.ERROR,
                message=issue.message,
                release_blocker=issue.severity in {"critical", "high"},
            )
        )
    no_core_override = all(entry.namespace != "core" for entry in matching)
    if not matching:
        findings.append(
            PluginCompatibilityFinding(
                check_id="mcp.mapping",
                passed=False,
                severity=PluginCompatibilitySeverity.WARNING,
                message="no MCP mapping entry matched this plugin",
            )
        )
    else:
        findings.append(
            PluginCompatibilityFinding(
                check_id="mcp.mapping",
                passed=validation.valid,
                severity=PluginCompatibilitySeverity.INFO
                if validation.valid
                else PluginCompatibilitySeverity.ERROR,
                message="MCP mapping is valid" if validation.valid else "MCP mapping has issues",
                release_blocker=not validation.valid,
            )
        )
    findings.append(
        PluginCompatibilityFinding(
            check_id="mcp.no_core_override",
            passed=no_core_override,
            severity=PluginCompatibilitySeverity.INFO
            if no_core_override
            else PluginCompatibilitySeverity.BLOCKER,
            message="MCP mapping does not override core tools"
            if no_core_override
            else "MCP mapping attempts to override core tools",
            release_blocker=not no_core_override,
        )
    )
    return (
        bool(matching) and validation.valid,
        no_core_override,
        [entry.exposed_tool_name for entry in matching],
    )


def _check_capability_catalog(
    manifest: PluginManifest | None,
    capability_entries: list[CapabilityEntry] | None,
    findings: list[PluginCompatibilityFinding],
) -> bool:
    if manifest is None or capability_entries is None:
        return True

    declared = {capability.capability_id for capability in manifest.capabilities}
    catalog = {entry.capability_id for entry in capability_entries}
    missing = sorted(declared - catalog)
    if missing:
        findings.append(
            PluginCompatibilityFinding(
                check_id="capability.catalog",
                passed=False,
                severity=PluginCompatibilitySeverity.WARNING,
                message=f"capabilities missing from supplied capability catalog: {missing}",
            )
        )
        return False
    findings.append(
        PluginCompatibilityFinding(
            check_id="capability.catalog",
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message="declared capabilities are present in supplied capability catalog",
        )
    )
    return True


def _check_paths_present(
    check_id: str,
    paths: list[Path],
    label: str,
    findings: list[PluginCompatibilityFinding],
) -> bool:
    if not paths:
        findings.append(
            PluginCompatibilityFinding(
                check_id=check_id,
                passed=False,
                severity=PluginCompatibilitySeverity.WARNING,
                message=f"no {label} declared",
            )
        )
        return False
    missing = sorted(str(path) for path in paths if not path.exists())
    if missing:
        findings.append(
            PluginCompatibilityFinding(
                check_id=check_id,
                passed=False,
                severity=PluginCompatibilitySeverity.ERROR,
                message=f"missing {label}: {missing}",
                release_blocker=True,
            )
        )
        return False
    findings.append(
        PluginCompatibilityFinding(
            check_id=check_id,
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message=f"{label} are declared and present",
        )
    )
    return True


def _check_old_project_naming(
    manifest_path: Path,
    docs: list[Path],
    findings: list[PluginCompatibilityFinding],
) -> bool:
    paths = [manifest_path, *docs]
    offenders: list[str] = []
    for path in paths:
        if path.exists() and OLD_PROJECT_NAME in path.read_text(encoding="utf-8"):
            offenders.append(str(path))
    if offenders:
        findings.append(
            PluginCompatibilityFinding(
                check_id="naming.old_project",
                passed=False,
                severity=PluginCompatibilitySeverity.BLOCKER,
                message=f"old project naming found in {offenders}",
                release_blocker=True,
            )
        )
        return False
    findings.append(
        PluginCompatibilityFinding(
            check_id="naming.old_project",
            passed=True,
            severity=PluginCompatibilitySeverity.INFO,
            message="old project naming was not found in checked files",
        )
    )
    return True


def _default_docs_for_manifest(manifest_path: Path) -> list[Path]:
    readme = manifest_path.parent / "README.md"
    return [readme] if readme.exists() else []


def _sandbox_permissions_for_manifest(manifest: PluginManifest) -> list[SandboxPermission]:
    permissions: list[SandboxPermission] = []
    for permission in manifest.required_permissions:
        mapped = PLUGIN_PERMISSION_TO_SANDBOX.get(permission)
        if mapped is not None:
            permissions.append(mapped)
    if not permissions:
        permissions.append(SandboxPermission.READ_PROJECT_FILES)
    return permissions


def _status_from_findings(
    findings: list[PluginCompatibilityFinding],
    matrix: PluginCompatibilityMatrix,
) -> PluginCompatibilityStatus:
    if any(finding.release_blocker for finding in findings):
        return PluginCompatibilityStatus.BLOCKED
    if matrix.all_passed:
        return PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    return PluginCompatibilityStatus.NEEDS_REVIEW
