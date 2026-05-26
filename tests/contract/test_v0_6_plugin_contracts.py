from __future__ import annotations

from pathlib import Path

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.extension_safety.models import (
    ExtensionPermission,
    ExtensionSafetyStatus,
)
from turing_research_plus.extension_safety.permission_policy import evaluate_permission
from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry
from turing_research_plus.plugins.registry import load_plugin_registry
from turing_research_plus.skill_market.catalog import build_skill_marketplace_index

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_CONTRACTS = [
    "contracts/plugin_architecture.yaml",
    "contracts/mcp_plugin_registry.yaml",
    "contracts/tool_capability_manifest.yaml",
    "contracts/skill_marketplace.yaml",
    "contracts/extension_safety.yaml",
]


def test_v0_6_plugin_system_contract_files_exist() -> None:
    for contract in REQUIRED_CONTRACTS:
        assert (ROOT / contract).exists()


def test_v0_6_plugin_docs_exist_and_state_boundaries() -> None:
    docs = [
        ROOT / "docs" / "plugin-architecture.md",
        ROOT / "docs" / "mcp-plugin-registry.md",
        ROOT / "docs" / "tool-capability-manifest.md",
        ROOT / "docs" / "skill-marketplace-layout.md",
        ROOT / "docs" / "extension-safety-gate.md",
    ]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        assert "No" in text or "does not" in text


def test_v0_6_plugin_system_registries_are_disabled_and_review_gated() -> None:
    plugin_registry = load_plugin_registry(ROOT / "examples" / "plugins")
    mcp_registry = load_mcp_plugin_registry(
        ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml"
    )

    assert plugin_registry.requires_human_review is True
    assert {
        plugin.plugin_id for plugin in plugin_registry.plugins if not plugin.third_party
    } <= {"trusted_local_demo_plugin"}
    assert all(plugin.status == "disabled" for plugin in plugin_registry.plugins)
    assert mcp_registry.requires_human_review is True
    assert all(entry.default_enabled is False for entry in mcp_registry.entries)
    assert all(entry.namespace != "core" for entry in mcp_registry.entries)


def test_v0_6_plugin_system_catalogs_are_aligned() -> None:
    capability_manifest = collect_capability_manifest()
    skill_market = build_skill_marketplace_index(ROOT / ".agents" / "skills")

    capability_categories = {entry.category.value for entry in capability_manifest.capabilities}
    skill_names = {entry.skill_name for entry in skill_market.entries}

    assert "plugin" in capability_categories
    assert "workspace" in capability_categories
    assert "turingresearch-master-orchestrator" in skill_names
    assert all(name.startswith("turingresearch-") for name in skill_names)


def test_v0_6_plugin_system_extension_policy_blocks_runtime_risks() -> None:
    execute_decision = evaluate_permission(ExtensionPermission.EXECUTE_CODE)
    remote_write_decision = evaluate_permission(ExtensionPermission.REMOTE_WRITE)
    network_decision = evaluate_permission(ExtensionPermission.NETWORK_ACCESS)

    assert execute_decision.status == ExtensionSafetyStatus.FORBIDDEN
    assert remote_write_decision.status == ExtensionSafetyStatus.FORBIDDEN
    assert network_decision.status == ExtensionSafetyStatus.RESTRICTED
