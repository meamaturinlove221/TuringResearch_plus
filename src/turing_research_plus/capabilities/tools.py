"""Local helper wrappers for capability manifests."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.capabilities.collector import collect_capability_manifest
from turing_research_plus.capabilities.manifest import write_capability_manifest_json
from turing_research_plus.capabilities.markdown_export import (
    render_capability_manifest_markdown,
)
from turing_research_plus.capabilities.models import CapabilityManifest


def capabilities_collect() -> CapabilityManifest:
    """Collect the static capability manifest."""

    return collect_capability_manifest()


def capabilities_markdown() -> str:
    """Render the static capability manifest as Markdown."""

    return render_capability_manifest_markdown(capabilities_collect())


def capabilities_export_json(output_path: Path) -> Path:
    """Write the static capability manifest as JSON."""

    return write_capability_manifest_json(capabilities_collect(), output_path)
