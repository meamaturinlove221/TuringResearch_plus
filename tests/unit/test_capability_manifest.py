from __future__ import annotations

import json

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.capabilities.manifest import (
    capability_manifest_to_dict,
    capability_manifest_to_json,
)


def test_capability_manifest_serializes_to_json_safe_dict() -> None:
    manifest = collect_capability_manifest()

    payload = capability_manifest_to_dict(manifest)

    assert payload["manifest_id"] == "turingresearch_capabilities"
    assert payload["starts_mcp_server"] is False
    assert payload["executes_tools"] is False
    assert len(payload["capabilities"]) >= 16


def test_capability_manifest_json_contains_expected_capability() -> None:
    manifest = collect_capability_manifest()

    payload = json.loads(capability_manifest_to_json(manifest))

    capability_ids = {entry["capability_id"] for entry in payload["capabilities"]}
    assert "plugin.registry" in capability_ids
    assert "workspace.registry" in capability_ids
    assert "remote_artifacts.unified" in capability_ids
