"""Capsule-local tool wrappers for hard gates."""

from __future__ import annotations

from typing import Any

from turing_research_plus.hard_gates.models import HardGateValidationInput
from turing_research_plus.hard_gates.validator import validate_hard_gates


def experiment_hard_gate_validate(request: HardGateValidationInput) -> dict[str, Any]:
    """Validate hard gates and return JSON-safe data."""

    return validate_hard_gates(request).model_dump(mode="json")
