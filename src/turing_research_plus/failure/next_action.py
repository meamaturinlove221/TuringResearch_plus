"""Next-action selection for failure categories."""

from __future__ import annotations

from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.failure.taxonomy import default_failure_taxonomy


def next_actions_for_category(category: FailureCategory) -> list[str]:
    """Return deterministic next actions for a failure category."""

    return list(default_failure_taxonomy()[category].default_next_actions)
