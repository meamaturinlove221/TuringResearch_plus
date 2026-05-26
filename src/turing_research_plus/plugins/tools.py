"""Local tool wrappers for plugin manifest validation."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.compat_report import PluginCompatibilityReport
from turing_research_plus.plugins.compat_test_runner import run_plugin_compatibility_check
from turing_research_plus.plugins.future_sandbox import (
    FutureSandboxRoadmap,
    build_future_sandbox_roadmap,
)
from turing_research_plus.plugins.loader import load_trusted_local_plugin
from turing_research_plus.plugins.loading_report import PluginLoadingReport
from turing_research_plus.plugins.manifest import load_plugin_manifest
from turing_research_plus.plugins.markdown_export import render_plugin_registry_markdown
from turing_research_plus.plugins.models import (
    PluginRegistry,
    PluginValidationReport,
)
from turing_research_plus.plugins.registry import load_plugin_registry
from turing_research_plus.plugins.risk_report import (
    PluginSandboxRiskReport,
    build_plugin_sandbox_report,
)
from turing_research_plus.plugins.sandbox_policy import SandboxPermission
from turing_research_plus.plugins.trust_policy import PluginTrustSource
from turing_research_plus.plugins.validator import validate_plugin_manifest


def plugin_validate(path: Path) -> PluginValidationReport:
    """Validate one plugin manifest without executing code."""

    return validate_plugin_manifest(load_plugin_manifest(path))


def plugin_registry_load(path: Path) -> PluginRegistry:
    """Load a local plugin registry from manifests."""

    return load_plugin_registry(path)


def plugin_registry_markdown(path: Path) -> str:
    """Render a local plugin registry as Markdown."""

    return render_plugin_registry_markdown(plugin_registry_load(path))


def plugin_trusted_load_plan(
    path: Path,
    *,
    source: PluginTrustSource = PluginTrustSource.WORKSPACE_LOCAL,
    explicit_trusted: bool = False,
    explicit_live: bool = False,
) -> PluginLoadingReport:
    """Build a trusted local plugin loading report without executing plugin code."""

    return load_trusted_local_plugin(
        path,
        source=source,
        explicit_trusted=explicit_trusted,
        explicit_live=explicit_live,
    )


def plugin_sandbox_check(
    plugin_id: str,
    permissions: list[SandboxPermission],
    *,
    explicit_enable: bool = False,
    scoped: bool = False,
) -> PluginSandboxRiskReport:
    """Build a plugin sandbox policy report without executing plugin code."""

    return build_plugin_sandbox_report(
        plugin_id,
        permissions,
        explicit_enable=explicit_enable,
        scoped=scoped,
    )


def plugin_future_sandbox_roadmap() -> FutureSandboxRoadmap:
    """Return future sandbox roadmap metadata."""

    return build_future_sandbox_roadmap()


def plugin_compatibility_check(
    manifest_path: Path,
    *,
    mcp_registry_path: Path | None = None,
    docs: list[Path] | None = None,
    tests: list[Path] | None = None,
) -> PluginCompatibilityReport:
    """Run a static plugin compatibility check without executing plugin code."""

    return run_plugin_compatibility_check(
        manifest_path,
        mcp_registry_path=mcp_registry_path,
        docs=docs,
        tests=tests,
    )
