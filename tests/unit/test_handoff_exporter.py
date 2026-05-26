from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.exporter import collect_handoff_files, export_handoff_bundle
from turing_research_plus.handoff.models import (
    HandoffBundleType,
    HandoffExportRequest,
    HandoffStatusLabel,
)


def test_exporter_includes_safe_files_and_omits_sensitive_files(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "summary.md").write_text("# Summary\n", encoding="utf-8")
    (source / ".env").write_text("API_KEY=secret\n", encoding="utf-8")
    (source / "SMPLX_NEUTRAL.npz").write_bytes(b"fake")

    manifest = export_handoff_bundle(
        HandoffExportRequest(
            bundle_id="bundle",
            source_root=source,
            output_dir=tmp_path / "out",
            file_paths=[
                Path("summary.md"),
                Path(".env"),
                Path("SMPLX_NEUTRAL.npz"),
                Path("missing.json"),
            ],
            source_machine_label="fixture-machine",
            bundle_type=HandoffBundleType.RUN_REVIEW,
            status_labels=[HandoffStatusLabel.REQUIRES_HUMAN_REVIEW],
        )
    )

    bundle = tmp_path / "out" / "bundle"
    assert (bundle / "summary.md").exists()
    assert not (bundle / ".env").exists()
    assert not (bundle / "SMPLX_NEUTRAL.npz").exists()
    assert (bundle / "HANDOFF_README.md").exists()
    assert (bundle / "handoff_manifest.yaml").exists()
    assert [item.relative_path for item in manifest.included_files] == ["summary.md"]
    assert {item.relative_path for item in manifest.omitted_files} == {
        ".env",
        "SMPLX_NEUTRAL.npz",
        "missing.json",
    }


def test_collect_handoff_files_preserves_relative_paths(tmp_path: Path) -> None:
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "report.md").write_text("x", encoding="utf-8")

    assert collect_handoff_files(tmp_path) == [Path("a") / "report.md"]
