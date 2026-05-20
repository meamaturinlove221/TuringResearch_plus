import pytest

from tuling_research_plus.subtask.models import (
    SubtaskErrorCode,
    SubtaskExecutionMode,
    SubtaskSpec,
    SubtaskStatus,
    TaskProfile,
)
from tuling_research_plus.subtask.prompts import render_role_prompt
from tuling_research_plus.subtask.runner import SubtaskRunner


def profile(quality_gate: str | None = "artifact_required") -> TaskProfile:
    return TaskProfile(
        name="architecture-reviewer",
        role="Architecture Reviewer",
        goal="Review a contract boundary in a single Codex window.",
        input_schema={"type": "object", "required": ["contract"]},
        output_schema={"type": "object", "required": ["findings"]},
        allowed_tools=["read_contract"],
        reasoning_style="skeptical and concise",
        quality_gate=quality_gate,
    )


def spec() -> SubtaskSpec:
    return SubtaskSpec(
        subtask_id="subtask-1",
        title="Review contract",
        inputs={"contract": "fusion_workflows"},
    )


def test_profile_validates_required_fields() -> None:
    task_profile = profile()

    assert task_profile.name == "architecture-reviewer"
    assert task_profile.profile_id == "architecture-reviewer"
    assert task_profile.input_schema["required"] == ["contract"]
    assert task_profile.output_schema["required"] == ["findings"]


def test_dry_run_returns_deterministic_output() -> None:
    result = SubtaskRunner().run(spec(), profile(), SubtaskExecutionMode.DRY_RUN)

    assert result.status == SubtaskStatus.COMPLETED
    assert result.artifacts[0].artifact_id == "artifact-subtask-1"
    assert result.artifacts[0].content["execution_mode"] == SubtaskExecutionMode.DRY_RUN


def test_role_prompt_rendered_for_manual_codex_role() -> None:
    rendered = render_role_prompt(spec(), profile())
    result = SubtaskRunner().run(
        spec(),
        profile(),
        SubtaskExecutionMode.MANUAL_CODEX_ROLE,
    )

    assert "Role: Architecture Reviewer" in rendered
    assert "Goal: Review a contract boundary" in result.rendered_prompt
    assert result.artifacts[0].artifact_id == "prompt-subtask-1"


def test_unsupported_llm_client_mode_raises_typed_error() -> None:
    with pytest.raises(ValueError, match="llm_client execution is not implemented"):
        SubtaskRunner().run(spec(), profile(), SubtaskExecutionMode.LLM_CLIENT)


def test_unknown_execution_mode_returns_typed_error() -> None:
    result = SubtaskRunner().run(spec(), profile(), "future_mode")

    assert result.status == SubtaskStatus.FAILED
    assert result.error is not None
    assert result.error.code == SubtaskErrorCode.UNSUPPORTED_EXECUTION_MODE
