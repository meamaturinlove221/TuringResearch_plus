import pytest

from turing_research_plus.hard_gates.models import GateOutcome, GateResult, HardGateValidationReport


def test_gate_result_non_pass_requires_reason() -> None:
    with pytest.raises(ValueError, match="non-pass"):
        GateResult(gate_id="no_promotion", outcome=GateOutcome.BLOCK)


def test_hard_gate_report_passed_property() -> None:
    report = HardGateValidationReport(
        report_id="report-1",
        results=[GateResult(gate_id="no_promotion", outcome=GateOutcome.PASS)],
        summary="ok",
    )

    assert report.passed is True
    assert "Passed: true" in report.to_markdown()
