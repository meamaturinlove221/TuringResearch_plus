"""No-delete/no-move/no-overwrite policy for shared stores."""

from __future__ import annotations

FORBIDDEN_ACTIONS = frozenset({"delete", "remove", "move", "rename", "overwrite", "write"})


def assert_read_only_action(action: str) -> None:
    """Raise when an action would mutate a shared store."""

    normalized = action.strip().lower()
    if normalized in FORBIDDEN_ACTIONS:
        raise PermissionError(f"shared store policy forbids action: {normalized}")


def is_read_only_action(action: str) -> bool:
    """Return whether the action is allowed by the no-delete policy."""

    return action.strip().lower() not in FORBIDDEN_ACTIONS
