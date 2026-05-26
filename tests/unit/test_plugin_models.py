from __future__ import annotations

import pytest

from turing_research_plus.plugins.models import (
    PluginCapability,
    PluginManifest,
    PluginRegistry,
    PluginSafetyLevel,
    PluginStatus,
    PluginType,
)


def _capability() -> PluginCapability:
    return PluginCapability(
        capability_id="demo",
        name="Demo",
        category="adapter",
        description="Demo capability.",
    )


def test_plugin_manifest_requires_permissions() -> None:
    with pytest.raises(ValueError, match="required permissions"):
        PluginManifest(
            plugin_id="demo_plugin",
            name="Demo Plugin",
            version="0.1.0",
            type=PluginType.ADAPTER,
            capabilities=[_capability()],
            safety_level=PluginSafetyLevel.PUBLIC_DEMO,
        )


def test_third_party_plugin_must_be_disabled() -> None:
    with pytest.raises(ValueError, match="third-party plugins"):
        PluginManifest(
            plugin_id="demo_plugin",
            name="Demo Plugin",
            version="0.1.0",
            type=PluginType.EXPORTER,
            capabilities=[_capability()],
            required_permissions=["read_demo"],
            safety_level=PluginSafetyLevel.PUBLIC_DEMO,
            status=PluginStatus.ENABLED,
            third_party=True,
        )


def test_plugin_registry_requires_unique_ids_and_review() -> None:
    plugin = PluginManifest(
        plugin_id="demo_plugin",
        name="Demo Plugin",
        version="0.1.0",
        type=PluginType.RENDERER,
        capabilities=[_capability()],
        required_permissions=["read_demo"],
        safety_level=PluginSafetyLevel.PUBLIC_DEMO,
    )

    with pytest.raises(ValueError, match="unique"):
        PluginRegistry(registry_id="demo", plugins=[plugin, plugin])
