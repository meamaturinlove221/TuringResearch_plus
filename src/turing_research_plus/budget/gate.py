"""Budget gate helpers."""

from turing_research_plus.budget.models import BudgetGate, BudgetGateStatus


def evaluate_budget_gate(gate: BudgetGate) -> BudgetGateStatus:
    """Evaluate a BudgetGate using its minimum ratio fields."""

    if gate.is_blocked:
        return BudgetGateStatus.BLOCKED
    if not gate.meets_minimum_ratio:
        return BudgetGateStatus.WARN
    return gate.status
