from __future__ import annotations

from pathlib import Path

from turing_research_plus.quality.metrics import (
    build_quality_report,
    evaluate_quality_metrics,
)

ROOT = Path(__file__).resolve().parents[2]


def test_quality_metrics_cover_required_dimensions() -> None:
    metrics = evaluate_quality_metrics(ROOT)
    ids = {metric.metric_id for metric in metrics}

    assert {
        "docs-completeness",
        "test-coverage-proxy",
        "contract-consistency",
        "example-readiness",
        "safety-readiness",
        "fake-live-boundary",
        "old-name-absence",
        "privacy-gate-pass",
        "release-readiness",
    } <= ids


def test_quality_report_is_reviewed_and_release_ready_when_metrics_pass() -> None:
    report = build_quality_report(ROOT)

    assert report.requires_human_review is True
    assert report.status in {"pass", "warn"}
    assert report.metrics
    assert all(0.0 <= metric.score <= 1.0 for metric in report.metrics)
