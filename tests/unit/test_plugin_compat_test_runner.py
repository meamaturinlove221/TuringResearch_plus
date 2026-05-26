from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.compat_report import PluginCompatibilityStatus
from turing_research_plus.plugins.compat_test_runner import (
    run_demo_plugin_compatibility,
    run_plugin_compatibility_check,
)

ROOT = Path(__file__).resolve().parents[2]


def test_run_plugin_compatibility_check_loads_mcp_registry() -> None:
    report = run_plugin_compatibility_check(
        ROOT / "examples" / "plugins" / "demo_exporter_plugin" / "plugin.yaml",
        mcp_registry_path=ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml",
        docs=[ROOT / "docs" / "plugin-architecture.md"],
        tests=[ROOT / "tests" / "workflow" / "test_mcp_plugin_registry_fake.py"],
    )

    assert report.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert report.matrix.mcp_mapping_valid is True
    assert report.mcp_tools == ["mcp.demo_export"]


def test_run_demo_plugin_compatibility_uses_repository_fixture() -> None:
    report = run_demo_plugin_compatibility(ROOT)

    assert report.plugin_id == "demo_exporter_plugin"
    assert report.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert report.matrix.all_passed is True
