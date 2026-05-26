from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRY_RUN = ROOT / "examples" / "vggt-human-prior-survey" / "real_run_ingest_dry_run"


def test_real_run_ingest_dry_run_records_missing_without_observed_claims() -> None:
    report = (DRY_RUN / "run_ingest_report.md").read_text(encoding="utf-8")
    updates = json.loads((DRY_RUN / "proposed_evidence_updates.json").read_text(encoding="utf-8"))
    missing = (DRY_RUN / "missing_artifacts.md").read_text(encoding="utf-8")

    assert "Did not modify VGGT project" in report
    assert "Did not run Modal" in report
    assert "local_project_links.yaml" in report
    assert updates[0]["status"] == "not-enough-evidence"
    assert "observed" not in updates[0]["status"]
    assert "real sparse backend log" in missing
    assert "V120 real run artifacts" in missing
    assert "V121 real run artifacts" in missing
