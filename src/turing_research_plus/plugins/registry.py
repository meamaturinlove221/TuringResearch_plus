"""Plugin registry helpers."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.manifest import load_plugin_manifest
from turing_research_plus.plugins.models import PluginManifest, PluginRegistry
from turing_research_plus.plugins.validator import validate_plugin_manifest


def load_plugin_registry(path: Path, *, registry_id: str = "local_plugins") -> PluginRegistry:
    """Load all plugin manifests under a directory without executing code."""

    manifests: list[PluginManifest] = []
    warnings: list[str] = []
    for manifest_path in sorted(path.rglob("plugin.yaml")):
        manifest = load_plugin_manifest(manifest_path)
        report = validate_plugin_manifest(manifest)
        if not report.valid:
            warnings.extend(
                f"{manifest.plugin_id}: {issue.message}" for issue in report.issues
            )
        manifests.append(manifest)

    return PluginRegistry(
        registry_id=registry_id,
        plugins=manifests,
        warnings=warnings,
        requires_human_review=True,
    )
