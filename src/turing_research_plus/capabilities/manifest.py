"""Capability manifest serialization helpers."""

from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.capabilities.models import CapabilityManifest


def capability_manifest_to_dict(manifest: CapabilityManifest) -> dict[str, object]:
    """Return a JSON-safe capability manifest mapping."""

    return manifest.model_dump(mode="json")


def capability_manifest_to_json(manifest: CapabilityManifest) -> str:
    """Serialize a capability manifest as stable JSON."""

    return json.dumps(capability_manifest_to_dict(manifest), indent=2, sort_keys=True)


def write_capability_manifest_json(manifest: CapabilityManifest, output_path: Path) -> Path:
    """Write a capability manifest JSON file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(capability_manifest_to_json(manifest) + "\n", encoding="utf-8")
    return output_path


def write_default_capability_manifest_json(output_path: Path) -> Path:
    """Collect and write the default capability manifest."""

    return write_capability_manifest_json(collect_capability_manifest(), output_path)
