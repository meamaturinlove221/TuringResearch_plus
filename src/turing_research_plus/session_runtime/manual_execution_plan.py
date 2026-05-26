"""Manual execution plan models for optional remote dry-run review."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ManualStepStatus(StrEnum):
    """Manual execution step status labels."""

    MANUAL_CONFIRMATION_REQUIRED = "manual-confirmation-required"
    BLOCKED = "blocked"


class ManualCommandStep(BaseModel):
    """One command reference that must be reviewed and run manually if ever used."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    command: str = Field(min_length=1)
    status: ManualStepStatus = ManualStepStatus.MANUAL_CONFIRMATION_REQUIRED
    requires_manual_confirmation: bool = True
    executes_in_turingresearch: bool = False
    remote_execution: bool = False
    notes: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def enforce_manual_only(self) -> Self:
        if self.executes_in_turingresearch:
            raise ValueError("manual command steps cannot execute in TuringResearch")
        if self.remote_execution:
            raise ValueError("manual command steps cannot enable remote execution")
        if not self.requires_manual_confirmation:
            raise ValueError("manual command steps require manual confirmation")
        return self


class RollbackPlanStep(BaseModel):
    """One manual rollback or cleanup reference."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(min_length=1)
    action: str = Field(min_length=1)
    manual_only: bool = True
    destructive: bool = False

    @model_validator(mode="after")
    def enforce_safe_rollback(self) -> Self:
        if not self.manual_only:
            raise ValueError("rollback steps must be manual-only")
        if self.destructive:
            raise ValueError("rollback plan cannot include destructive commands")
        return self


class HumanConfirmationChecklist(BaseModel):
    """Checklist that must be completed before any human remote attempt."""

    model_config = ConfigDict(extra="forbid")

    items: list[str] = Field(default_factory=list)
    all_required: bool = True
    human_review_required: bool = True


def build_default_manual_commands(remote_target_placeholder: str) -> list[ManualCommandStep]:
    """Build commented command references for a future human remote attempt."""

    return [
        ManualCommandStep(
            step_id="manual-review-target",
            title="Review remote target placeholder",
            command=f"# MANUAL ONLY: confirm target {remote_target_placeholder}",
            notes=["Do not run if the target host, directory, or user is unclear."],
        ),
        ManualCommandStep(
            step_id="manual-transfer-reference",
            title="Transfer context pack manually",
            command="# MANUAL ONLY: sftp put ./context_pack/* <reviewed-target>/",
            notes=["This is a reference only; TuringResearch does not run SFTP."],
        ),
        ManualCommandStep(
            step_id="manual-launch-reference",
            title="Launch remote work manually",
            command="# MANUAL ONLY: run reviewed command in a separate human shell",
            notes=["No SSH, tmux, Modal, or remote command is run by this plan."],
        ),
        ManualCommandStep(
            step_id="manual-return-reference",
            title="Collect structured return manually",
            command="# MANUAL ONLY: copy return files into a local review directory",
            notes=["Return files must be verified before any ingest review."],
        ),
    ]


def build_default_rollback_plan() -> list[RollbackPlanStep]:
    """Build non-destructive manual rollback guidance."""

    return [
        RollbackPlanStep(
            step_id="stop-before-transfer",
            action="If preflight or context pack review fails, do not transfer files.",
        ),
        RollbackPlanStep(
            step_id="archive-local-plan",
            action="Keep the local dry-run report for audit instead of deleting remote files.",
        ),
        RollbackPlanStep(
            step_id="request-human-cleanup",
            action="If a human created remote files, cleanup must be reviewed and run manually.",
        ),
    ]


def build_default_confirmation_checklist() -> HumanConfirmationChecklist:
    """Build the default human confirmation checklist."""

    return HumanConfirmationChecklist(
        items=[
            "Preflight report is pass or pass-with-warnings, not blocked.",
            "Forbidden files are excluded from the context pack.",
            "Remote target placeholder has been replaced outside the repo.",
            "No secret, raw data, or restricted model payload will be transferred.",
            "Manual commands have been reviewed by a human.",
            "Return artifact requirements are understood before remote work starts.",
            "No automatic Evidence Ledger write will occur.",
        ]
    )


def render_manual_execution_plan(
    commands: list[ManualCommandStep],
    rollback_steps: list[RollbackPlanStep],
    checklist: HumanConfirmationChecklist,
) -> str:
    """Render manual command references and confirmations as Markdown."""

    lines = [
        "## Manual Command References",
        "",
        "These commands are references only. TuringResearch does not execute them.",
        "",
    ]
    for item in commands:
        lines.extend(
            [
                f"### {item.title}",
                "",
                f"- Step: `{item.step_id}`",
                f"- Status: `{item.status}`",
                "- Requires manual confirmation: `true`",
                "- Executes in TuringResearch: `false`",
                "- Remote execution enabled: `false`",
                "",
                "```bash",
                item.command,
                "```",
                "",
            ]
        )
        if item.notes:
            lines.extend(["Notes:", *[f"- {note}" for note in item.notes], ""])

    lines.extend(["## Rollback Plan", ""])
    for rollback_item in rollback_steps:
        lines.append(f"- `{rollback_item.step_id}`: {rollback_item.action}")

    lines.extend(["", "## Human Confirmation Checklist", ""])
    lines.extend([f"- [ ] {item}" for item in checklist.items] or ["- [ ] No checklist items."])
    return "\n".join(lines) + "\n"
