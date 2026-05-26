from __future__ import annotations

from pathlib import Path

from turing_research_plus.plugins import PluginTrustSource, load_trusted_local_plugin

ROOT = Path(__file__).resolve().parents[2]
DEMO_PLUGIN = ROOT / "examples" / "plugins" / "trusted_local_demo_plugin" / "plugin.yaml"


def test_trusted_local_plugin_loading_fake_workflow() -> None:
    report = load_trusted_local_plugin(
        DEMO_PLUGIN,
        source=PluginTrustSource.BUILT_IN_DEMO,
    )

    assert report.plugin_id == "trusted_local_demo_plugin"
    assert report.loaded is True
    assert report.requires_human_review is True
    assert report.exposed_capabilities[0].disabled_by_default is True
    assert report.executes_code is False
    assert report.loads_entrypoint is False
    assert report.safety_report is not None
    assert report.safety_report.loads_third_party_code is False
