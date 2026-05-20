from tuling_research_plus.subtask.models import (
    SubtaskErrorCode,
    SubtaskExecutionMode,
    SubtaskSpec,
    SubtaskStatus,
    TaskProfile,
)
from tuling_research_plus.subtask.quality import evaluate_quality_gate
from tuling_research_plus.subtask.runner import SubtaskRunner


def test_quality_gate_failure_detected() -> None:
    result = SubtaskRunner().run(
        SubtaskSpec(subtask_id="subtask-1", title="Quality gate failure"),
        TaskProfile(
            name="strict-profile",
            role="Strict Reviewer",
            goal="Fail on unknown gates.",
            input_schema={"type": "object"},
            output_schema={"type": "object"},
            quality_gate="unknown_gate",
        ),
        SubtaskExecutionMode.DRY_RUN,
    )

    assert result.status == SubtaskStatus.FAILED
    assert result.error is not None
    assert result.error.code == SubtaskErrorCode.QUALITY_GATE_FAILED


def test_quality_gate_passes_when_artifact_required() -> None:
    profile = TaskProfile(
        name="artifact-profile",
        role="Artifact Reviewer",
        goal="Require artifact output.",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
        quality_gate="artifact_required",
    )
    result = SubtaskRunner().run(
        SubtaskSpec(subtask_id="subtask-1", title="Artifact gate"),
        profile,
        SubtaskExecutionMode.DRY_RUN,
    )

    assert evaluate_quality_gate(result, profile) is True
