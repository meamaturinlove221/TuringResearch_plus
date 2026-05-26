from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.capabilities.markdown_export import (
    render_capability_manifest_markdown,
)
from turing_research_plus.capabilities.tools import (
    capabilities_collect,
    capabilities_export_json,
    capabilities_markdown,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "capabilities" / "turingresearch_capabilities.json"


def test_capability_manifest_fixture_is_fake_static_and_complete() -> None:
    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    categories = {entry["category"] for entry in payload["capabilities"]}

    assert payload["generated_from_static_catalog"] is True
    assert payload["starts_mcp_server"] is False
    assert payload["executes_tools"] is False
    assert payload["requires_human_review"] is True
    assert {
        "evidence",
        "artifact",
        "visual",
        "advisor",
        "pdf",
        "paper",
        "citation",
        "collision",
        "related work",
        "route",
        "failure",
        "dashboard",
        "remote artifact",
        "handoff",
        "plugin",
        "workspace",
    }.issubset(categories)


def test_capability_manifest_helpers_do_not_execute_tools(tmp_path: Path) -> None:
    manifest = capabilities_collect()
    markdown = capabilities_markdown()
    output_path = capabilities_export_json(tmp_path / "capabilities.json")

    exported = json.loads(output_path.read_text(encoding="utf-8"))

    assert manifest.executes_tools is False
    assert manifest.starts_mcp_server is False
    assert "does not execute tools" in markdown
    assert exported["manifest_id"] == "turingresearch_capabilities"


def test_capability_manifest_runtime_matches_fixture_categories() -> None:
    runtime_manifest = collect_capability_manifest()
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
    runtime_markdown = render_capability_manifest_markdown(runtime_manifest)

    runtime_categories = {entry.category.value for entry in runtime_manifest.capabilities}
    fixture_categories = {entry["category"] for entry in fixture["capabilities"]}

    assert runtime_categories == fixture_categories
    assert "plugin.registry" in runtime_markdown
