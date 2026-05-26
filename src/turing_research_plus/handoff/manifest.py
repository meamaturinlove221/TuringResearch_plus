"""Manifest helpers for handoff bundles."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from turing_research_plus.handoff.models import HandoffBundleManifest


def sha256_file(path: Path) -> str:
    """Compute sha256 for one local file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_manifest(manifest: HandoffBundleManifest) -> str:
    """Compute manifest-level sha256 from included file records."""

    digest = hashlib.sha256()
    for record in sorted(manifest.included_files, key=lambda item: item.relative_path):
        digest.update(record.relative_path.encode("utf-8"))
        digest.update((record.sha256 or "").encode("utf-8"))
    return digest.hexdigest()


def manifest_to_yaml(manifest: HandoffBundleManifest) -> str:
    """Render a YAML-compatible JSON manifest without requiring PyYAML."""

    return manifest.model_dump_json(indent=2) + "\n"


def manifest_from_yaml(text: str) -> HandoffBundleManifest:
    """Parse manifests emitted by manifest_to_yaml."""

    data = json.loads(text)
    return HandoffBundleManifest.model_validate(data)
