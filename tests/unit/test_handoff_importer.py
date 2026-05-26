from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.exporter import export_handoff_bundle
from turing_research_plus.handoff.importer import import_handoff_bundle
from turing_research_plus.handoff.models import HandoffExportRequest, HandoffImportRequest


def test_importer_validates_manifest_and_sha256(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "report.md").write_text("review only\n", encoding="utf-8")
    export_handoff_bundle(
        HandoffExportRequest(
            bundle_id="bundle",
            source_root=source,
            output_dir=tmp_path / "out",
            file_paths=[Path("report.md")],
        )
    )

    report = import_handoff_bundle(HandoffImportRequest(bundle_dir=tmp_path / "out" / "bundle"))

    assert report.valid_manifest is True
    assert report.verified_files == ["report.md"]
    assert report.is_usable_for_review is True
    assert report.proposed_updates[0]["status"] == "requires-human-review"


def test_importer_reports_missing_file(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "report.md").write_text("review only\n", encoding="utf-8")
    export_handoff_bundle(
        HandoffExportRequest(
            bundle_id="bundle",
            source_root=source,
            output_dir=tmp_path / "out",
            file_paths=[Path("report.md")],
        )
    )
    (tmp_path / "out" / "bundle" / "report.md").unlink()

    report = import_handoff_bundle(HandoffImportRequest(bundle_dir=tmp_path / "out" / "bundle"))

    assert report.missing_files == ["report.md"]
    assert report.is_usable_for_review is False


def test_importer_reports_sha256_mismatch(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "report.md").write_text("review only\n", encoding="utf-8")
    export_handoff_bundle(
        HandoffExportRequest(
            bundle_id="bundle",
            source_root=source,
            output_dir=tmp_path / "out",
            file_paths=[Path("report.md")],
        )
    )
    (tmp_path / "out" / "bundle" / "report.md").write_text("tampered\n", encoding="utf-8")

    report = import_handoff_bundle(HandoffImportRequest(bundle_dir=tmp_path / "out" / "bundle"))

    assert report.sha256_mismatches == ["report.md"]
