from turing_research_plus.budget.gate import evaluate_budget_gate
from turing_research_plus.budget.models import (
    BudgetGate,
    BudgetGateStatus,
    BudgetLimit,
    BudgetUnit,
    BudgetUsage,
)


def test_budget_gate_tracks_blocked_status() -> None:
    gate = BudgetGate(
        gate_id="budget-1",
        limits=[BudgetLimit(unit=BudgetUnit.REQUESTS, limit=10)],
        usage=[BudgetUsage(unit=BudgetUnit.REQUESTS, used=10)],
        status=BudgetGateStatus.BLOCKED,
    )

    assert gate.is_blocked is True
    assert gate.dry_run_allowed is True


def test_budget_gate_tracks_target_current_ratio_and_deviation_reason() -> None:
    gate = BudgetGate(
        gate_id="budget-2",
        target=100,
        current=40,
        minimum_ratio=0.5,
        deviation_reason="Below planned evidence coverage.",
        limits=[BudgetLimit(unit=BudgetUnit.TOKENS, limit=1000)],
    )

    assert gate.ratio == 0.4
    assert gate.meets_minimum_ratio is False
    assert gate.deviation_reason == "Below planned evidence coverage."
    assert evaluate_budget_gate(gate) == BudgetGateStatus.WARN
