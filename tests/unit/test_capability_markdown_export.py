from __future__ import annotations

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.capabilities.markdown_export import (
    render_capability_manifest_markdown,
)


def test_capability_markdown_export_contains_safety_boundary() -> None:
    markdown = render_capability_manifest_markdown(collect_capability_manifest())

    assert "Capability Manifest: turingresearch_capabilities" in markdown
    assert "does not execute tools" in markdown
    assert "does not start an MCP server" in markdown
    assert "remote_artifacts.unified" in markdown
    assert "related_work.positioning" in markdown
