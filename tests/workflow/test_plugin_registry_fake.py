from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.tools import (
    plugin_registry_load,
    plugin_registry_markdown,
    plugin_validate,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "examples" / "plugins"


def test_plugin_registry_fake_validates_manifest_only_plugins() -> None:
    registry = plugin_registry_load(FIXTURES)
    markdown = plugin_registry_markdown(FIXTURES)
    report = plugin_validate(FIXTURES / "demo_adapter_plugin" / "plugin.yaml")

    assert {plugin.plugin_id for plugin in registry.plugins} >= {
        "demo_adapter_plugin",
        "demo_exporter_plugin",
        "trusted_local_demo_plugin",
    }
    assert registry.requires_human_review is True
    assert registry.disabled_plugins == [
        "demo_adapter_plugin",
        "demo_exporter_plugin",
        "trusted_local_demo_plugin",
    ]
    assert report.valid is True
    assert report.executes_code is False
    assert report.loads_entrypoint is False
    assert "Third-party plugins remain disabled by default" in markdown
