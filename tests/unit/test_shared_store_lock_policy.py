from __future__ import annotations

from turing_research_plus.shared_store.lock_policy import evaluate_lock_status
from turing_research_plus.shared_store.models import SharedStoreLockStatus


def test_lock_policy_not_required_by_default(tmp_path) -> None:
    assert evaluate_lock_status(tmp_path) == SharedStoreLockStatus.NOT_REQUIRED


def test_lock_policy_detects_missing_and_present_lock(tmp_path) -> None:
    assert (
        evaluate_lock_status(tmp_path, require_lock_file=True)
        == SharedStoreLockStatus.LOCK_MISSING
    )

    (tmp_path / ".turingresearch_shared_store.lock").write_text("read-only\n", encoding="utf-8")

    assert (
        evaluate_lock_status(tmp_path, require_lock_file=True)
        == SharedStoreLockStatus.LOCK_PRESENT
    )
