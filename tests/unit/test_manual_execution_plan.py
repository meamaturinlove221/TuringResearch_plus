from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.session_runtime.manual_execution_plan import (
    ManualCommandStep,
    RollbackPlanStep,
    build_default_confirmation_checklist,
    build_default_manual_commands,
    build_default_rollback_plan,
    render_manual_execution_plan,
)


def test_default_manual_commands_are_reference_only() -> None:
    commands = build_default_manual_commands("<user>@<host>:/target")

    assert commands
    assert all(command.requires_manual_confirmation for command in commands)
    assert all(not command.executes_in_turingresearch for command in commands)
    assert all(not command.remote_execution for command in commands)
    assert all(command.command.startswith("# MANUAL ONLY:") for command in commands)


def test_manual_command_rejects_enabled_remote_execution() -> None:
    with pytest.raises(ValidationError):
        ManualCommandStep(
            step_id="bad",
            title="bad",
            command="ssh host",
            remote_execution=True,
        )


def test_rollback_plan_rejects_destructive_action() -> None:
    with pytest.raises(ValidationError):
        RollbackPlanStep(
            step_id="delete-remote",
            action="delete remote files",
            destructive=True,
        )


def test_render_manual_execution_plan_lists_checklist() -> None:
    text = render_manual_execution_plan(
        build_default_manual_commands("<user>@<host>:/target"),
        build_default_rollback_plan(),
        build_default_confirmation_checklist(),
    )

    assert "Manual Command References" in text
    assert "TuringResearch does not execute" in text
    assert "Human Confirmation Checklist" in text
    assert "No automatic Evidence Ledger write will occur" in text
