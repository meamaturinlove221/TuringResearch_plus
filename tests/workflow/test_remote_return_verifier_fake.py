from __future__ import annotations

from pathlib import Path

from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierStatus,
    verify_return_package,
)

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "session_runtime" / "return_fixture"


def test_remote_return_verifier_fake_fixture_passes_review_gate() -> None:
    report = verify_return_package(FIXTURE, return_id="return-fixture")

    assert report.status == ReturnVerifierStatus.PASS
    assert report.release_blocker is False
    assert report.missing_artifacts == []
    assert report.unsafe_files == []
    assert report.checksum_mismatches == []
    assert report.auto_write_evidence_ledger is False
    assert report.proposed_updates_only is True
    assert report.requires_human_review is True
    assert report.proposed_updates.updates[0].status == "proposed"
