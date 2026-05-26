from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.plugins.local_plugin import ExposedPluginCapability, LocalPlugin
from turing_research_plus.plugins.models import (
    PluginCapability,
    PluginManifest,
    PluginSafetyLevel,
    PluginStatus,
    PluginType,
)
from turing_research_plus.plugins.trust_policy import PluginTrustSource, evaluate_plugin_trust


def plugin_manifest() -> PluginManifest:
    return PluginManifest(
        plugin_id="trusted_demo",
        name="Trusted Demo",
        version="0.1.0",
        type=PluginType.EXPORTER,
        capabilities=[
            PluginCapability(
                capability_id="demo_export",
                name="Demo Export",
                category="exporter",
                description="Demo export metadata.",
            )
        ],
        required_permissions=["read_demo_markdown"],
        safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        status=PluginStatus.DISABLED,
        third_party=False,
    )


def test_exposed_capability_is_disabled_by_default() -> None:
    capability = ExposedPluginCapability.from_capability(plugin_manifest().capabilities[0])

    assert capability.disabled_by_default is True
    assert capability.fake_mode is True


def test_local_plugin_wraps_metadata_only_manifest() -> None:
    manifest = plugin_manifest()
    local_plugin = LocalPlugin(
        manifest=manifest,
        manifest_path=Path("plugin.yaml"),
        trust_decision=evaluate_plugin_trust(
            manifest,
            source=PluginTrustSource.BUILT_IN_DEMO,
        ),
        exposed_capabilities=[
            ExposedPluginCapability.from_capability(manifest.capabilities[0])
        ],
    )

    assert local_plugin.executes_code is False
    assert local_plugin.loads_entrypoint is False
    assert local_plugin.exposed_capabilities[0].disabled_by_default is True


def test_local_plugin_rejects_disallowed_trust_decision() -> None:
    manifest = plugin_manifest()
    with pytest.raises(ValueError, match="allowed trust decision"):
        LocalPlugin(
            manifest=manifest,
            manifest_path=Path("plugin.yaml"),
            trust_decision=evaluate_plugin_trust(
                manifest,
                source=PluginTrustSource.WORKSPACE_LOCAL,
            ),
        )
