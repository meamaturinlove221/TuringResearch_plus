from __future__ import annotations

from pathlib import Path

from turing_research_plus.mcp_plugins.models import MCPPluginEntry, MCPPluginRegistry
from turing_research_plus.plugins.compat_report import PluginCompatibilityStatus
from turing_research_plus.plugins.compatibility import check_plugin_compatibility
from turing_research_plus.plugins.models import PluginSafetyLevel

ROOT = Path(__file__).resolve().parents[2]
DEMO_PLUGIN = ROOT / "examples" / "plugins" / "demo_exporter_plugin" / "plugin.yaml"
DEMO_DOC = ROOT / "docs" / "plugin-architecture.md"
DEMO_TEST = ROOT / "tests" / "workflow" / "test_mcp_plugin_registry_fake.py"


def _demo_registry(namespace: str = "mcp") -> MCPPluginRegistry:
    return MCPPluginRegistry(
        registry_id="demo_registry",
        entries=[
            MCPPluginEntry(
                plugin_id="demo_exporter_plugin",
                exposed_tool_name=f"{namespace}.demo_export",
                namespace=namespace,
                input_schema="DemoExportInput",
                output_schema="DemoExportOutput",
                permissions=["read_demo_markdown", "write_demo_export_manifest"],
                safety_level=PluginSafetyLevel.PUBLIC_DEMO,
                default_enabled=False,
                third_party=True,
                docs=["docs/plugin-architecture.md"],
                tests=["tests/workflow/test_mcp_plugin_registry_fake.py"],
            )
        ],
    )


def test_plugin_compatibility_accepts_demo_manifest_with_review() -> None:
    report = check_plugin_compatibility(
        DEMO_PLUGIN,
        mcp_registry=_demo_registry(),
        docs=[DEMO_DOC],
        tests=[DEMO_TEST],
    )

    assert report.plugin_id == "demo_exporter_plugin"
    assert report.status == PluginCompatibilityStatus.COMPATIBLE_WITH_REVIEW
    assert report.matrix.all_passed is True
    assert report.mcp_tools == ["mcp.demo_export"]
    assert report.executes_plugin_code is False
    assert report.enables_plugin is False


def test_plugin_compatibility_marks_missing_docs_and_tests_as_review_needed() -> None:
    report = check_plugin_compatibility(
        DEMO_PLUGIN,
        mcp_registry=_demo_registry(),
        docs=[],
        tests=[],
    )

    assert report.status == PluginCompatibilityStatus.NEEDS_REVIEW
    assert report.matrix.docs_present is False
    assert report.matrix.tests_declared is False
    assert any(finding.check_id == "docs.present" for finding in report.findings)


def test_plugin_compatibility_blocks_forbidden_permission(tmp_path: Path) -> None:
    manifest = tmp_path / "plugin.yaml"
    manifest.write_text(
        "\n".join(
            [
                "plugin_id: unsafe_plugin",
                "name: Unsafe Plugin",
                "version: 0.1.0",
                "type: exporter",
                "entry_kind: manifest-only",
                "safety_level: public-demo",
                "status: disabled",
                "third_party: true",
                "executes_code: false",
                "required_permissions:",
                "  - execute_code",
                "config_schema:",
                "capabilities:",
                "  - capability_id: unsafe_capability",
                "    name: Unsafe Capability",
                "    category: exporter",
                "    description: Unsafe fixture.",
                "inputs:",
                "  - Input",
                "outputs:",
                "  - Output",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    report = check_plugin_compatibility(manifest, docs=[DEMO_DOC], tests=[DEMO_TEST])

    assert report.status == PluginCompatibilityStatus.BLOCKED
    assert report.matrix.no_forbidden_permission is False
    assert any(finding.check_id == "permissions.forbidden" for finding in report.findings)


def test_plugin_compatibility_treats_missing_mcp_mapping_as_review_needed() -> None:
    report = check_plugin_compatibility(
        DEMO_PLUGIN,
        docs=[DEMO_DOC],
        tests=[DEMO_TEST],
    )

    assert report.status == PluginCompatibilityStatus.NEEDS_REVIEW
    assert report.matrix.mcp_mapping_valid is False
    assert report.matrix.no_core_tool_override is True
