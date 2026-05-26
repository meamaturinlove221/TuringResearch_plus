from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.artifact_summary import build_artifact_summary

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_build_artifact_summary_parses_demo_table() -> None:
    summary = build_artifact_summary(DEMO / "demo_artifact_index.md")

    assert summary.selected_count == 2
    assert summary.omitted_count == 1
    assert summary.missing_count == 1
    assert summary.no_raw_data is True
    assert any(record.artifact == "raw/private_dataset.zip" for record in summary.records)
