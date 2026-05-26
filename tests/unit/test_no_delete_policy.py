from __future__ import annotations

import pytest

from turing_research_plus.shared_store.no_delete_policy import (
    assert_read_only_action,
    is_read_only_action,
)


def test_no_delete_policy_allows_read_actions() -> None:
    assert is_read_only_action("scan")
    assert is_read_only_action("read")
    assert_read_only_action("index")


def test_no_delete_policy_blocks_mutating_actions() -> None:
    for action in ["delete", "remove", "move", "rename", "overwrite", "write"]:
        assert not is_read_only_action(action)
        with pytest.raises(PermissionError, match="forbids action"):
            assert_read_only_action(action)
