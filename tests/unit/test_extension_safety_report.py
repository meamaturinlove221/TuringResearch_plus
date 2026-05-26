from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionKind,
    ExtensionManifestRef,
    ExtensionPermission,
)
from turing_research_plus.extension_safety.report import (
    render_extension_safety_report_markdown,
)
from turing_research_plus.extension_safety.validator import validate_extension_safety


def test_extension_safety_report_markdown_states_no_execution() -> None:
    manifest = ExtensionManifestRef(
        extension_id="demo_mcp_plugin",
        kind=ExtensionKind.MCP_PLUGIN,
        third_party=True,
        default_enabled=False,
        requested_permissions=[ExtensionPermission.READ_LOCAL_FILES],
        declared_safety_level="public-demo",
        has_manifest=True,
        has_safety_report=True,
    )
    report = validate_extension_safety(manifest)
    markdown = render_extension_safety_report_markdown(report)

    assert "Extension Safety Report: demo_mcp_plugin" in markdown
    assert "Executes extension code: `false`" in markdown
    assert "Loads third-party code: `false`" in markdown
    assert "does not grant runtime permissions" in markdown
