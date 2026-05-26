"""Optional remote dry-run plan for Session runtime production parity."""

from __future__ import annotations

from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime.archive_safety import (
    audit_context_pack_candidates,
)
from turing_research_plus.session_runtime.context_manifest import (
    ContextPackOmittedFile,
)
from turing_research_plus.session_runtime.manual_execution_plan import (
    HumanConfirmationChecklist,
    ManualCommandStep,
    RollbackPlanStep,
    build_default_confirmation_checklist,
    build_default_manual_commands,
    build_default_rollback_plan,
    render_manual_execution_plan,
)
from turing_research_plus.session_runtime.models import (
    SessionPreflightReport,
    SessionPreflightRequest,
    SessionPreflightStatus,
)
from turing_research_plus.session_runtime.preflight_runner import run_session_preflight
from turing_research_plus.session_runtime.return_manifest import REQUIRED_RETURN_FILES


class RemoteDryRunStatus(StrEnum):
    """Remote dry-run plan status labels."""

    READY_FOR_HUMAN_REVIEW = "ready-for-human-review"
    READY_WITH_WARNINGS = "ready-with-warnings"
    BLOCKED = "blocked"


class RemoteDryRunFileRecord(BaseModel):
    """One file selected for a possible manual transfer."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    source_path: str | None = None
    size_bytes: int = 0
    transfer_mode: str = "manual-reference-only"


class RemoteDryRunPlanRequest(BaseModel):
    """Request for a local remote dry-run plan."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    plan_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    project_root: Path
    context_source: Path
    output_dir: Path
    remote_target_placeholder: str = "<user>@<host>:/reviewed/target/path"
    source_platform: str = "Windows"
    target_platform: str = "Linux pod"
    allow_raw_data: bool = False
    remote_execution_enabled: bool = False
    live_network_enabled: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_dry_run_only(self) -> Self:
        if self.remote_execution_enabled:
            raise ValueError("remote dry-run plan cannot enable remote execution")
        if self.live_network_enabled:
            raise ValueError("remote dry-run plan cannot enable live networking")
        if not self.requires_human_review:
            raise ValueError("remote dry-run plan requires human review")
        return self


class RemoteDryRunPlan(BaseModel):
    """Review-only plan for a possible manual remote pod attempt."""

    model_config = ConfigDict(extra="forbid")

    plan_id: str = Field(min_length=1)
    status: RemoteDryRunStatus
    preflight: SessionPreflightReport
    files_to_transfer: list[RemoteDryRunFileRecord] = Field(default_factory=list)
    forbidden_files_excluded: list[ContextPackOmittedFile] = Field(default_factory=list)
    remote_target_placeholder: str = Field(min_length=1)
    manual_commands: list[ManualCommandStep] = Field(default_factory=list)
    rollback_plan: list[RollbackPlanStep] = Field(default_factory=list)
    return_artifact_requirements: list[str] = Field(
        default_factory=lambda: list(REQUIRED_RETURN_FILES)
    )
    human_confirmation_checklist: HumanConfirmationChecklist = Field(
        default_factory=build_default_confirmation_checklist
    )
    ssh_enabled: bool = False
    sftp_enabled: bool = False
    tmux_enabled: bool = False
    modal_enabled: bool = False
    remote_execution_enabled: bool = False
    dry_run_only: bool = True
    automatic_evidence_write: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_safe_boundaries(self) -> Self:
        if self.ssh_enabled or self.sftp_enabled or self.tmux_enabled or self.modal_enabled:
            raise ValueError("remote dry-run plan cannot enable live remote transports")
        if self.remote_execution_enabled:
            raise ValueError("remote dry-run plan cannot enable remote execution")
        if not self.dry_run_only:
            raise ValueError("remote dry-run plan must stay dry-run only")
        if self.automatic_evidence_write:
            raise ValueError("remote dry-run plan cannot write evidence automatically")
        if not self.requires_human_review:
            raise ValueError("remote dry-run plan requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether the plan is blocked before human remote review."""

        return self.status == RemoteDryRunStatus.BLOCKED


def build_remote_dry_run_plan(request: RemoteDryRunPlanRequest) -> RemoteDryRunPlan:
    """Build a dry-run plan without opening network or executing remote commands."""

    lifecycle = PodContextLifecycle(
        context_package_id=request.package_id,
        source_machine_label="local-dry-run-machine",
        target_environment_label="manual-remote-placeholder",
        route_id=request.route_id,
    )
    preflight = run_session_preflight(
        SessionPreflightRequest(
            session_id=request.session_id,
            project_root=request.project_root,
            context_source=request.context_source,
            output_dir=request.output_dir,
            lifecycle=lifecycle,
            source_platform=request.source_platform,
            target_platform=request.target_platform,
            allow_raw_data=request.allow_raw_data,
        )
    )
    safety = audit_context_pack_candidates(
        request.context_source,
        allow_raw_data=request.allow_raw_data,
    )
    selected = [
        RemoteDryRunFileRecord(
            path=check.archive_path,
            source_path=check.source_path,
            size_bytes=check.file_size,
        )
        for check in safety.checks
        if check.included
    ]
    omitted = [
        ContextPackOmittedFile(path=check.archive_path, reasons=check.reasons)
        for check in safety.checks
        if not check.included
    ]

    return RemoteDryRunPlan(
        plan_id=request.plan_id,
        status=_status_from_preflight(preflight.status, omitted),
        preflight=preflight,
        files_to_transfer=selected,
        forbidden_files_excluded=omitted,
        remote_target_placeholder=request.remote_target_placeholder,
        manual_commands=build_default_manual_commands(request.remote_target_placeholder),
        rollback_plan=build_default_rollback_plan(),
        return_artifact_requirements=list(REQUIRED_RETURN_FILES),
    )


def render_remote_dry_run_plan(plan: RemoteDryRunPlan) -> str:
    """Render a remote dry-run plan for human review."""

    lines = [
        f"# Optional Remote Dry-run Plan: {plan.plan_id}",
        "",
        f"- Status: `{plan.status}`",
        f"- Session: `{plan.preflight.session_id}`",
        f"- Package: `{plan.preflight.context_package_id}`",
        f"- Route: `{plan.preflight.route_id}`",
        f"- Remote target placeholder: `{plan.remote_target_placeholder}`",
        "- SSH enabled: `false`",
        "- SFTP enabled: `false`",
        "- tmux enabled: `false`",
        "- Modal enabled: `false`",
        "- Remote execution enabled: `false`",
        "- Dry-run only: `true`",
        "- Automatic Evidence Ledger write: `false`",
        "- Requires human review: `true`",
        "",
        "## Preflight Result",
        "",
        f"- Preflight status: `{plan.preflight.status}`",
        f"- Release blocker: `{str(plan.preflight.release_blocker).lower()}`",
        "",
        "## Files To Transfer",
        "",
    ]
    lines.extend(
        [
            f"- `{item.path}` ({item.size_bytes} bytes) `{item.transfer_mode}`"
            for item in plan.files_to_transfer
        ]
        or ["- None."]
    )
    lines.extend(["", "## Forbidden Files Excluded", ""])
    lines.extend(
        [
            f"- `{item.path}`: {', '.join(item.reasons) if item.reasons else 'unspecified'}"
            for item in plan.forbidden_files_excluded
        ]
        or ["- None."]
    )
    lines.extend(["", "## Return Artifact Requirements", ""])
    lines.extend([f"- `{item}`" for item in plan.return_artifact_requirements])
    lines.extend(
        [
            "",
            render_manual_execution_plan(
                plan.manual_commands,
                plan.rollback_plan,
                plan.human_confirmation_checklist,
            ).rstrip(),
            "",
        ]
    )
    return "\n".join(lines)


def write_remote_dry_run_plan(plan: RemoteDryRunPlan, output_path: Path) -> Path:
    """Write a remote dry-run plan Markdown file."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_remote_dry_run_plan(plan), encoding="utf-8")
    return output_path


def _status_from_preflight(
    status: SessionPreflightStatus,
    omitted: list[ContextPackOmittedFile],
) -> RemoteDryRunStatus:
    if status == SessionPreflightStatus.BLOCKED:
        return RemoteDryRunStatus.BLOCKED
    if status == SessionPreflightStatus.PASS_WITH_WARNINGS or omitted:
        return RemoteDryRunStatus.READY_WITH_WARNINGS
    return RemoteDryRunStatus.READY_FOR_HUMAN_REVIEW
