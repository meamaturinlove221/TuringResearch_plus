from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.capabilities.models import CapabilityCategory
from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry
from turing_research_plus.mcp_plugins.validator import validate_mcp_plugin_registry
from turing_research_plus.plugins.compat_report import PluginCompatibilityStatus
from turing_research_plus.plugins.compat_test_runner import run_demo_plugin_compatibility
from turing_research_plus.plugins.loader import load_trusted_local_plugin
from turing_research_plus.plugins.permission_gate import evaluate_sandbox_permission
from turing_research_plus.plugins.sandbox_policy import (
    SandboxDecisionStatus,
    SandboxPermission,
)
from turing_research_plus.plugins.trust_policy import PluginTrustSource

ROOT = Path(__file__).resolve().parents[2]
TRUSTED_DEMO = ROOT / "examples" / "plugins" / "trusted_local_demo_plugin" / "plugin.yaml"
MCP_REGISTRY = ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"


def test_v0_7_plugin_system_end_to_end_fake_chain() -> None:
    loading_report = load_trusted_local_plugin(
        TRUSTED_DEMO,
        source=PluginTrustSource.BUILT_IN_DEMO,
    )
    sandbox_execute = evaluate_sandbox_permission(SandboxPermission.EXECUTE_CODE)
    sandbox_secrets_access_decision = evaluate_sandbox_permission(
        SandboxPermission.SECRETS_ACCESS
    )
    compatibility_report = run_demo_plugin_compatibility(ROOT)
    mcp_registry = load_mcp_plugin_registry(MCP_REGISTRY)
    mcp_report = validate_mcp_plugin_registry(mcp_registry)
    capability_manifest = collect_capability_manifest()
    mcp_config = json.loads((ROOT / ".mcp.example.json").read_text(encoding="utf-8"))
    distribution_doc = (ROOT / "docs" / "mcp-distribution-guide.md").read_text(
        encoding="utf-8"
    )

    assert loading_report.loaded is True
    assert loading_report.executes_code is False
    assert loading_report.loads_entrypoint is False
    assert loading_report.exposed_capabilities[0].disabled_by_default is True
    assert loading_report.safety_report is not None
    assert loading_report.safety_report.loads_third_party_code is False

    assert sandbox_execute.status == SandboxDecisionStatus.DENIED
    assert sandbox_execute.release_blocker is True
    assert sandbox_secrets_access_decision.status == SandboxDecisionStatus.DENIED
    assert sandbox_secrets_access_decision.release_blocker is True

    assert compatibility_report.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert compatibility_report.matrix.all_passed is True
    assert compatibility_report.executes_plugin_code is False
    assert compatibility_report.starts_mcp_server is False
    assert compatibility_report.enables_plugin is False

    assert mcp_report.valid is True
    assert mcp_report.starts_mcp_server is False
    assert mcp_report.loads_plugin_code is False
    assert all(entry.default_enabled is False for entry in mcp_registry.entries)
    assert all(entry.namespace != "core" for entry in mcp_registry.entries)

    assert CapabilityCategory.PLUGIN in capability_manifest.categories
    assert capability_manifest.starts_mcp_server is False
    assert capability_manifest.executes_tools is False

    server = mcp_config["mcpServers"]["turingresearch-plus"]
    assert server["env"]["TURINGRESEARCH_ENABLE_LIVE_TESTS"] == "0"
    assert server["env"]["TURINGRESEARCH_ENABLE_PLUGINS"] == "0"
    assert server["env"]["TURINGRESEARCH_ENABLE_PLUGIN_LIVE_MODE"] == "0"
    assert server["env"]["GITHUB_TOKEN"] in {"", "PLACEHOLDER"}
    assert "plugin tools disabled by default" in distribution_doc
    assert "Live mode is optional" in distribution_doc
