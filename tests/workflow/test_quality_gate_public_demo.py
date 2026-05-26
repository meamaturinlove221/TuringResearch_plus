from __future__ import annotations

from pathlib import Path

from turing_research_plus.quality.metrics import build_quality_report
from turing_research_plus.quality.regression_gate import run_regression_gate

ROOT = Path(__file__).resolve().parents[2]


def test_quality_gate_public_demo_is_release_safe_by_policy() -> None:
    quality = build_quality_report(ROOT)
    gate = run_regression_gate(ROOT)

    assert gate.status == "pass"
    assert gate.blockers == []
    assert any(metric.metric_id == "example-readiness" for metric in quality.metrics)
    assert any(metric.metric_id == "fake-live-boundary" for metric in quality.metrics)
    assert quality.requires_human_review is True
    assert gate.requires_human_review is True
