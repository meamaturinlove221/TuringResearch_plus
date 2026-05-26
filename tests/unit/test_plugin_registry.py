from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.markdown_export import render_plugin_registry_markdown
from turing_research_plus.plugins.registry import load_plugin_registry

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "examples" / "plugins"


def test_load_plugin_registry_from_demo_fixtures() -> None:
    registry = load_plugin_registry(FIXTURES, registry_id="demo_plugins")

    assert registry.registry_id == "demo_plugins"
    assert {plugin.plugin_id for plugin in registry.plugins} >= {
        "demo_adapter_plugin",
        "demo_exporter_plugin",
        "trusted_local_demo_plugin",
    }
    assert registry.disabled_plugins == [
        "demo_adapter_plugin",
        "demo_exporter_plugin",
        "trusted_local_demo_plugin",
    ]
    assert registry.requires_human_review is True


def test_plugin_registry_markdown_states_safety_boundary() -> None:
    registry = load_plugin_registry(FIXTURES)
    markdown = render_plugin_registry_markdown(registry)

    assert "Plugin code is not executed" in markdown
    assert "Unknown Python entrypoints are not loaded" in markdown
    assert "demo_exporter_plugin" in markdown
