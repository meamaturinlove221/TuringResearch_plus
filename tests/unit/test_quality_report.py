from __future__ import annotations

from pathlib import Path

from turing_research_plus.quality.metrics import build_quality_report
from turing_research_plus.quality.regression_gate import run_regression_gate
from turing_research_plus.quality.report import (
    render_quality_report_markdown,
    render_regression_gate_markdown,
)

ROOT = Path(__file__).resolve().parents[2]


def test_render_quality_report_markdown_contains_metrics() -> None:
    report = build_quality_report(ROOT)
    markdown = render_quality_report_markdown(report)

    assert "# Quality Report:" in markdown
    assert "`docs-completeness`" in markdown
    assert "`contract-consistency`" in markdown
    assert "Requires human review" in markdown


def test_render_regression_gate_markdown_contains_boundaries() -> None:
    report = run_regression_gate(ROOT)
    markdown = render_regression_gate_markdown(report)

    assert "# Regression Gate Report:" in markdown
    assert "`old-name-absence`" in markdown
    assert "`live-tests-default-skip`" in markdown
    assert "It does not publish or tag a release." in markdown
