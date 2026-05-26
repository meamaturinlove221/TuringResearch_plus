from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.compat_report import PluginCompatibilityStatus
from turing_research_plus.plugins.compat_test_runner import run_demo_plugin_compatibility
from turing_research_plus.plugins.tools import plugin_compatibility_check

ROOT = Path(__file__).resolve().parents[2]


def test_demo_plugin_compatibility_workflow() -> None:
    report = run_demo_plugin_compatibility(ROOT)

    assert report.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert report.matrix.manifest_schema_valid is True
    assert report.matrix.capability_ids_valid is True
    assert report.matrix.required_permissions_declared is True
    assert report.matrix.safety_policy_satisfied is True
    assert report.matrix.mcp_mapping_valid is True
    assert report.matrix.docs_present is True
    assert report.matrix.tests_declared is True
    assert report.matrix.no_core_tool_override is True
    assert report.matrix.no_old_project_naming is True
    assert report.matrix.no_forbidden_permission is True
    assert report.requires_human_review is True
    assert report.executes_plugin_code is False
    assert report.loads_entrypoint is False
    assert report.starts_mcp_server is False
    assert report.enables_plugin is False


def test_plugin_compatibility_tool_wrapper_is_static() -> None:
    report = plugin_compatibility_check(
        ROOT / "examples" / "plugins" / "demo_exporter_plugin" / "plugin.yaml",
        mcp_registry_path=ROOT / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml",
        docs=[ROOT / "docs" / "plugin-architecture.md"],
        tests=[ROOT / "tests" / "workflow" / "test_demo_plugin_compatibility.py"],
    )

    assert report.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert "mcp.demo_export" in report.mcp_tools
