from turing_research_plus.subtask.models import SubtaskSpec, SubtaskStatus, TaskProfile
from turing_research_plus.subtask.runner import SubtaskRunner


def test_task_profile_accepts_dry_run_without_tools() -> None:
    profile = TaskProfile(
        name="profile-1",
        role="research-worker",
        goal="Return a deterministic fixture.",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )

    assert profile.dry_run is True
    assert profile.max_steps == 1
    assert profile.profile_id == "profile-1"


def test_subtask_runner_returns_fake_artifact() -> None:
    result = SubtaskRunner().run(
        SubtaskSpec(subtask_id="subtask-1", title="Fake subtask"),
        TaskProfile(
            name="profile-1",
            role="research-worker",
            goal="Return a deterministic fixture.",
            input_schema={"type": "object"},
            output_schema={"type": "object"},
        ),
    )

    assert result.status == SubtaskStatus.COMPLETED
    assert result.artifacts[0].artifact_id == "artifact-subtask-1"
    assert result.artifacts[0].evidence[0].source_id == "subtask:subtask-1"
