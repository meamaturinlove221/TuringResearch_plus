from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.importer import import_handoff_bundle
from turing_research_plus.handoff.manifest import manifest_from_yaml
from turing_research_plus.handoff.models import HandoffImportRequest

FIXTURE = Path("examples") / "vggt-human-prior-survey" / "handoff_bundle_fixture"


def test_vggt_handoff_fixture_manifest_is_review_only() -> None:
    manifest = manifest_from_yaml((FIXTURE / "handoff_manifest.yaml").read_text(encoding="utf-8"))

    assert manifest.project_name == "TuringResearch Plus"
    assert manifest.manual_review_required is True
    assert "requires-human-review" in {str(item) for item in manifest.status_labels}
    assert manifest.omitted_files


def test_vggt_handoff_fixture_import_report() -> None:
    report = import_handoff_bundle(HandoffImportRequest(bundle_dir=FIXTURE))

    assert report.valid_manifest is True
    assert "HANDOFF_README.md" in report.verified_files
    assert report.proposed_updates[0]["status"] == "requires-human-review"
    assert report.manual_review_required is True
