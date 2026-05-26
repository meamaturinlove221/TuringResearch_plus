from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.loader import load_trusted_local_plugin
from turing_research_plus.plugins.trust_policy import PluginTrustSource, PluginTrustStatus

ROOT = Path(__file__).resolve().parents[2]
DEMO_PLUGIN = ROOT / "examples" / "plugins" / "trusted_local_demo_plugin" / "plugin.yaml"


def test_loads_built_in_demo_plugin_manifest_without_execution() -> None:
    report = load_trusted_local_plugin(
        DEMO_PLUGIN,
        source=PluginTrustSource.BUILT_IN_DEMO,
    )

    assert report.loaded is True
    assert report.validation_report.valid is True
    assert report.trust_decision.status == PluginTrustStatus.ALLOWED
    assert report.safety_report is not None
    assert report.safety_report.executes_extension_code is False
    assert report.exposed_capabilities
    assert all(capability.disabled_by_default for capability in report.exposed_capabilities)
    assert report.executes_code is False
    assert report.loads_entrypoint is False


def test_workspace_local_plugin_requires_explicit_trusted_flag() -> None:
    report = load_trusted_local_plugin(
        DEMO_PLUGIN,
        source=PluginTrustSource.WORKSPACE_LOCAL,
    )

    assert report.loaded is False
    assert report.trust_decision.status == PluginTrustStatus.DISABLED_BY_DEFAULT
    assert report.errors

    trusted = load_trusted_local_plugin(
        DEMO_PLUGIN,
        source=PluginTrustSource.WORKSPACE_LOCAL,
        explicit_trusted=True,
    )
    assert trusted.loaded is True


def test_network_plugin_requires_explicit_live_flag(tmp_path: Path) -> None:
    plugin = tmp_path / "plugin.yaml"
    plugin.write_text(
        "\n".join(
            [
                "plugin_id: live_demo",
                "name: Live Demo",
                "version: 0.1.0",
                "type: adapter",
                "entry_kind: manifest-only",
                "safety_level: live-optional",
                "status: disabled",
                "third_party: false",
                "executes_code: false",
                "required_permissions:",
                "  - network_access",
                "config_schema:",
                "capabilities:",
                "  - capability_id: live_demo_capability",
                "    name: Live Demo Capability",
                "    category: adapter",
                "    description: Live optional metadata only.",
                "inputs:",
                "  - DemoInput",
                "outputs:",
                "  - DemoOutput",
            ]
        ),
        encoding="utf-8",
    )

    report = load_trusted_local_plugin(plugin, source=PluginTrustSource.BUILT_IN_DEMO)

    assert report.loaded is False
    assert report.trust_decision.status == PluginTrustStatus.REQUIRES_LIVE_FLAG

    live = load_trusted_local_plugin(
        plugin,
        source=PluginTrustSource.BUILT_IN_DEMO,
        explicit_live=True,
    )
    assert live.loaded is True
    assert "network_access requires explicit human approval" in live.warnings


def test_execute_code_manifest_is_rejected_by_validation(tmp_path: Path) -> None:
    plugin = tmp_path / "plugin.yaml"
    plugin.write_text(
        "\n".join(
            [
                "plugin_id: unsafe_demo",
                "name: Unsafe Demo",
                "version: 0.1.0",
                "type: workflow",
                "entry_kind: manifest-only",
                "safety_level: restricted",
                "status: disabled",
                "third_party: false",
                "executes_code: true",
                "required_permissions:",
                "  - execute_code",
                "config_schema:",
                "capabilities:",
                "inputs:",
                "outputs:",
            ]
        ),
        encoding="utf-8",
    )

    report = load_trusted_local_plugin(plugin, source=PluginTrustSource.BUILT_IN_DEMO)

    assert report.loaded is False
    assert report.validation_report.valid is False
    assert report.trust_decision.status == PluginTrustStatus.BLOCKED
    assert report.errors
