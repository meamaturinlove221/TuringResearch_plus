from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.evidence_summary import build_evidence_summary

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_build_evidence_summary_counts_statuses() -> None:
    summary = build_evidence_summary(DEMO / "demo_evidence_ledger.json")

    assert summary.ledger_id == "public_demo_evidence_ledger"
    assert summary.status == "demo-only"
    assert summary.status_counts["planned"] == 1
    assert summary.status_counts["fake-data"] == 1
    assert summary.status_counts["not-enough-evidence"] == 1
    assert "observed" not in summary.status_counts
