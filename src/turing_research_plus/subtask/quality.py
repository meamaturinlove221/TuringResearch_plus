"""Quality gates for subtask runtime."""

from __future__ import annotations

from turing_research_plus.subtask.models import SubtaskResult, SubtaskStatus, TaskProfile


def evaluate_quality_gate(result: SubtaskResult, profile: TaskProfile) -> bool:
    """Evaluate built-in quality gates for deterministic subtask tests."""

    if profile.quality_gate is None:
        return True
    if profile.quality_gate == "artifact_required":
        return bool(result.artifacts)
    if profile.quality_gate == "completed_status":
        return result.status == SubtaskStatus.COMPLETED
    return False
