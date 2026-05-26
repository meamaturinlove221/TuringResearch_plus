from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.manifest import (
    manifest_from_yaml,
    manifest_to_yaml,
    sha256_file,
    sha256_manifest,
)
from turing_research_plus.handoff.models import (
    HandoffBundleManifest,
    HandoffBundleType,
    HandoffFileRecord,
)


def test_manifest_round_trips_without_pyyaml() -> None:
    manifest = HandoffBundleManifest(
        bundle_id="bundle-a",
        source_machine_label="main",
        bundle_type=HandoffBundleType.RUN_REVIEW,
        included_files=[HandoffFileRecord(relative_path="report.md", sha256="abc")],
    )
    manifest.sha256 = sha256_manifest(manifest)

    parsed = manifest_from_yaml(manifest_to_yaml(manifest))

    assert parsed.bundle_id == "bundle-a"
    assert parsed.included_files[0].relative_path == "report.md"
    assert parsed.sha256 == manifest.sha256


def test_sha256_file(tmp_path: Path) -> None:
    path = tmp_path / "a.txt"
    path.write_text("abc", encoding="utf-8")

    assert sha256_file(path) == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
