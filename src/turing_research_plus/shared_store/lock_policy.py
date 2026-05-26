"""Lock-file policy for local mounted shared stores."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.shared_store.models import SharedStoreLockStatus


def evaluate_lock_status(
    root_path: Path,
    *,
    require_lock_file: bool = False,
    lock_file_name: str = ".turingresearch_shared_store.lock",
) -> SharedStoreLockStatus:
    """Evaluate a local lock file without creating or modifying it."""

    if not require_lock_file:
        return SharedStoreLockStatus.NOT_REQUIRED
    lock_path = root_path / lock_file_name
    if not lock_path.exists():
        return SharedStoreLockStatus.LOCK_MISSING
    if not lock_path.is_file():
        return SharedStoreLockStatus.LOCK_UNREADABLE
    try:
        lock_path.read_text(encoding="utf-8")
    except OSError:
        return SharedStoreLockStatus.LOCK_UNREADABLE
    return SharedStoreLockStatus.LOCK_PRESENT
