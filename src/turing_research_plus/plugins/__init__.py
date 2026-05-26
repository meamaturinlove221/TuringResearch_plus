"""Plugin manifest registry and validation helpers."""

from turing_research_plus.plugins.demo_plugins import DEMO_PLUGIN_ID, DEMO_PLUGIN_PATH
from turing_research_plus.plugins.future_sandbox import (
    FutureSandboxMilestone,
    FutureSandboxRoadmap,
    build_future_sandbox_roadmap,
)
from turing_research_plus.plugins.loader import load_trusted_local_plugin
from turing_research_plus.plugins.loading_report import PluginLoadingReport
from turing_research_plus.plugins.local_plugin import ExposedPluginCapability, LocalPlugin
from turing_research_plus.plugins.manifest import load_plugin_manifest
from turing_research_plus.plugins.markdown_export import render_plugin_registry_markdown
from turing_research_plus.plugins.models import (
    PluginCapability,
    PluginEntryKind,
    PluginManifest,
    PluginRegistry,
    PluginSafetyLevel,
    PluginStatus,
    PluginType,
    PluginValidationIssue,
    PluginValidationReport,
)
from turing_research_plus.plugins.permission_gate import (
    evaluate_sandbox_permission,
    evaluate_sandbox_permissions,
)
from turing_research_plus.plugins.registry import load_plugin_registry
from turing_research_plus.plugins.risk_report import (
    PluginSandboxRiskReport,
    build_plugin_sandbox_report,
)
from turing_research_plus.plugins.sandbox_policy import (
    PluginSandboxPolicy,
    SandboxDecisionStatus,
    SandboxPermission,
    SandboxPermissionDecision,
    SandboxRiskLevel,
    default_plugin_sandbox_policy,
)
from turing_research_plus.plugins.trust_policy import (
    PluginTrustDecision,
    PluginTrustSource,
    PluginTrustStatus,
    evaluate_plugin_trust,
)
from turing_research_plus.plugins.validator import validate_plugin_manifest

__all__ = [
    "DEMO_PLUGIN_ID",
    "DEMO_PLUGIN_PATH",
    "ExposedPluginCapability",
    "FutureSandboxMilestone",
    "FutureSandboxRoadmap",
    "LocalPlugin",
    "PluginCapability",
    "PluginEntryKind",
    "PluginLoadingReport",
    "PluginManifest",
    "PluginRegistry",
    "PluginSafetyLevel",
    "PluginSandboxPolicy",
    "PluginSandboxRiskReport",
    "PluginStatus",
    "PluginTrustDecision",
    "PluginTrustSource",
    "PluginTrustStatus",
    "PluginType",
    "PluginValidationIssue",
    "PluginValidationReport",
    "SandboxDecisionStatus",
    "SandboxPermission",
    "SandboxPermissionDecision",
    "SandboxRiskLevel",
    "build_future_sandbox_roadmap",
    "build_plugin_sandbox_report",
    "default_plugin_sandbox_policy",
    "evaluate_sandbox_permission",
    "evaluate_sandbox_permissions",
    "evaluate_plugin_trust",
    "load_plugin_manifest",
    "load_plugin_registry",
    "load_trusted_local_plugin",
    "render_plugin_registry_markdown",
    "validate_plugin_manifest",
]
