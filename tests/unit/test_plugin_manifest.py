from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins.manifest import load_plugin_manifest
from turing_research_plus.plugins.models import PluginStatus, PluginType

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "plugins" / "demo_exporter_plugin" / "plugin.yaml"


def test_load_plugin_manifest_from_demo_yaml() -> None:
    manifest = load_plugin_manifest(FIXTURE)

    assert manifest.plugin_id == "demo_exporter_plugin"
    assert manifest.type == PluginType.EXPORTER
    assert manifest.status == PluginStatus.DISABLED
    assert manifest.third_party is True
    assert manifest.executes_code is False
    assert manifest.python_entrypoint is None
    assert manifest.required_permissions
    assert manifest.capabilities[0].capability_id == "demo_markdown_export"
