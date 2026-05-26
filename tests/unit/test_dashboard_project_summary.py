from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard_api.project_summary import build_project_summary

ROOT = Path(__file__).resolve().parents[2]
DEMO = ROOT / "examples" / "public_demo"


def test_build_project_summary_from_public_demo() -> None:
    summary = build_project_summary(DEMO / "demo_research_intent.md")

    assert summary.title == "Demo Research Intent"
    assert summary.status == "demo only."
    assert "fictional geometry-aware model adapter" in summary.topic
    assert summary.demo_only is True
    assert summary.read_only is True
