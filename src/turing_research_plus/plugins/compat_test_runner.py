"""Compatibility test runner for local plugin fixtures."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.mcp_plugins.registry import load_mcp_plugin_registry
from turing_research_plus.plugins.compat_report import PluginCompatibilityReport
from turing_research_plus.plugins.compatibility import check_plugin_compatibility


def run_plugin_compatibility_check(
    manifest_path: Path,
    *,
    mcp_registry_path: Path | None = None,
    docs: list[Path] | None = None,
    tests: list[Path] | None = None,
) -> PluginCompatibilityReport:
    """Run a local static compatibility check for one plugin manifest."""

    registry = load_mcp_plugin_registry(mcp_registry_path) if mcp_registry_path else None
    return check_plugin_compatibility(
        manifest_path,
        mcp_registry=registry,
        docs=docs,
        tests=tests,
    )


def run_demo_plugin_compatibility(root: Path) -> PluginCompatibilityReport:
    """Run the repository demo exporter plugin compatibility check."""

    return run_plugin_compatibility_check(
        root / "examples" / "plugins" / "demo_exporter_plugin" / "plugin.yaml",
        mcp_registry_path=root / "examples" / "plugins" / "demo_mcp_plugin" / "registry.yaml",
        docs=[
            root / "docs" / "plugin-architecture.md",
            root / "docs" / "mcp-plugin-registry.md",
        ],
        tests=[
            root / "tests" / "workflow" / "test_mcp_plugin_registry_fake.py",
            root / "tests" / "workflow" / "test_demo_plugin_compatibility.py",
        ],
    )
