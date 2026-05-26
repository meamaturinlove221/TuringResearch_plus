"""Fake-first pod workflow replay runtime.

This module composes the local session runtime pieces into one deterministic
replay chain. It never opens SSH, runs remote commands, or applies evidence
updates.
"""

from __future__ import annotations

import shutil
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.pod_lifecycle.transfer_policy import transfer_warnings_for_path
from turing_research_plus.session_runtime.archive_safety import normalize_pack_entry
from turing_research_plus.session_runtime.archive_writer import sha256_file
from turing_research_plus.session_runtime.context_manifest import ContextPackManifest
from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
    build_context_pack,
)
from turing_research_plus.session_runtime.models import (
    SessionPreflightReport,
    SessionPreflightRequest,
    SessionPreflightStatus,
)
from turing_research_plus.session_runtime.preflight_runner import run_session_preflight
from turing_research_plus.session_runtime.proposed_updates import ProposedUpdateLoadReport
from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierReport,
    verify_return_package,
)
from turing_research_plus.session_runtime.transfer_report import (
    TransferFileRecord,
    TransferMode,
    TransferOmittedFile,
    TransferReport,
)
from turing_research_plus.session_runtime.transfer_runner import (
    TransferRunnerRequest,
    run_transfer,
)


class PodWorkflowReplayStatus(StrEnum):
    """Status for a full fake pod workflow replay."""

    PASS = "pass"
    PASS_WITH_WARNINGS = "pass-with-warnings"
    BLOCKED = "blocked"


class FakePodReturnFixtureReport(BaseModel):
    """Report for copying a fake pod return fixture into replay workspace."""

    model_config = ConfigDict(extra="forbid")

    return_id: str = Field(min_length=1)
    source_dir: str = Field(min_length=1)
    target_dir: str = Field(min_length=1)
    copied_files: list[TransferFileRecord] = Field(default_factory=list)
    omitted_files: list[TransferOmittedFile] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    live_ssh_enabled: bool = False
    remote_command_execution: bool = False
    contains_secrets: bool = False
    contains_raw_data: bool = False
    contains_model_payloads: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_fake_return_boundary(self) -> Self:
        if self.live_ssh_enabled:
            raise ValueError("fake pod return fixture cannot enable live SSH")
        if self.remote_command_execution:
            raise ValueError("fake pod return fixture cannot execute remote commands")
        if self.contains_secrets:
            raise ValueError("fake pod return fixture cannot contain secrets")
        if self.contains_raw_data:
            raise ValueError("fake pod return fixture cannot contain raw data")
        if self.contains_model_payloads:
            raise ValueError("fake pod return fixture cannot contain model payloads")
        if not self.requires_human_review:
            raise ValueError("fake pod return fixture requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether fixture copy blocks replay review."""

        return bool(self.errors)


class PodWorkflowReplayRequest(BaseModel):
    """Request for a local fake pod workflow replay."""

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    replay_id: str = Field(min_length=1)
    session_id: str = Field(min_length=1)
    package_id: str = Field(min_length=1)
    route_id: str = Field(min_length=1)
    project_root: Path
    preflight_context_source: Path
    preflight_output_dir: Path
    context_pack_source_dir: Path
    replay_workspace: Path
    fake_return_fixture_dir: Path
    project_name: str = "TuringResearch Plus"
    source_platform: str = "Windows"
    target_platform: str = "Linux pod"
    archive_format: str = "tar"
    live_ssh_enabled: bool = False
    live_network_enabled: bool = False
    remote_command_execution: bool = False
    automatic_ledger_write: bool = False
    allow_raw_data: bool = False
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_fake_replay_boundary(self) -> Self:
        if self.live_ssh_enabled:
            raise ValueError("pod workflow replay cannot enable live SSH")
        if self.live_network_enabled:
            raise ValueError("pod workflow replay cannot enable live networking")
        if self.remote_command_execution:
            raise ValueError("pod workflow replay cannot execute remote commands")
        if self.automatic_ledger_write:
            raise ValueError("pod workflow replay cannot auto-write the Evidence Ledger")
        if self.allow_raw_data:
            raise ValueError("pod workflow replay cannot allow raw data")
        if not self.requires_human_review:
            raise ValueError("pod workflow replay requires human review")
        return self


class PodWorkflowReplayReport(BaseModel):
    """Review-only report for the full fake pod workflow replay chain."""

    model_config = ConfigDict(extra="forbid")

    replay_id: str = Field(min_length=1)
    status: PodWorkflowReplayStatus
    preflight: SessionPreflightReport
    context_pack: ContextPackManifest
    transfer: TransferReport
    fake_return: FakePodReturnFixtureReport
    return_verifier: ReturnVerifierReport
    proposed_evidence_update_report: ProposedUpdateLoadReport
    chain: list[str] = Field(default_factory=list)
    live_ssh_enabled: bool = False
    live_network_enabled: bool = False
    remote_command_execution: bool = False
    automatic_ledger_write: bool = False
    proposed_updates_only: bool = True
    requires_human_review: bool = True

    @model_validator(mode="after")
    def enforce_replay_report_boundary(self) -> Self:
        if self.live_ssh_enabled:
            raise ValueError("pod workflow replay report cannot enable live SSH")
        if self.live_network_enabled:
            raise ValueError("pod workflow replay report cannot enable live networking")
        if self.remote_command_execution:
            raise ValueError("pod workflow replay report cannot execute remote commands")
        if self.automatic_ledger_write:
            raise ValueError("pod workflow replay report cannot auto-write ledger")
        if not self.proposed_updates_only:
            raise ValueError("pod workflow replay report must stay proposed-only")
        if not self.requires_human_review:
            raise ValueError("pod workflow replay report requires human review")
        return self

    @property
    def release_blocker(self) -> bool:
        """Return whether any replay stage blocks review."""

        return self.status == PodWorkflowReplayStatus.BLOCKED


def run_pod_workflow_replay(request: PodWorkflowReplayRequest) -> PodWorkflowReplayReport:
    """Run local fake replay: preflight, pack, transfer, fake return, verify."""

    lifecycle = PodContextLifecycle(
        context_package_id=request.package_id,
        source_machine_label="local-fake-replay-machine",
        target_environment_label="fake-pod-return-fixture",
        route_id=request.route_id,
    )
    preflight = run_session_preflight(
        SessionPreflightRequest(
            session_id=request.session_id,
            project_root=request.project_root,
            context_source=request.preflight_context_source,
            output_dir=request.preflight_output_dir,
            lifecycle=lifecycle,
            source_platform=request.source_platform,
            target_platform=request.target_platform,
            archive_format=request.archive_format,
        )
    )

    context_pack_dir = request.replay_workspace / "context_pack"
    context_pack = build_context_pack(
        ContextPackBuildRequest(
            package_id=request.package_id,
            route_id=request.route_id,
            source_dir=request.context_pack_source_dir,
            output_dir=context_pack_dir,
            project_name=request.project_name,
        )
    )

    fake_transfer_target = request.replay_workspace / "fake_transfer_target"
    transfer = run_transfer(
        TransferRunnerRequest(
            transfer_id=f"{request.replay_id}-fake-transfer",
            package_id=request.package_id,
            source_dir=context_pack_dir,
            target=fake_transfer_target.as_posix(),
            mode=TransferMode.FAKE,
        )
    )

    fake_return_dir = request.replay_workspace / "fake_pod_return"
    fake_return = copy_fake_pod_return_fixture(
        return_id=f"{request.replay_id}-fake-return",
        source_dir=request.fake_return_fixture_dir,
        target_dir=fake_return_dir,
    )
    verifier = verify_return_package(
        fake_return_dir,
        return_id=f"{request.replay_id}-return-verifier",
    )

    status = _overall_status(preflight, context_pack, transfer, fake_return, verifier)
    return PodWorkflowReplayReport(
        replay_id=request.replay_id,
        status=status,
        preflight=preflight,
        context_pack=context_pack,
        transfer=transfer,
        fake_return=fake_return,
        return_verifier=verifier,
        proposed_evidence_update_report=verifier.proposed_updates,
        chain=[
            "SessionPreflightRunner",
            "ContextPackBuilder",
            "FakeTransferRunner",
            "FakePodReturnFixture",
            "RemoteReturnVerifier",
            "ProposedEvidenceUpdateReport",
        ],
        live_ssh_enabled=False,
        live_network_enabled=False,
        remote_command_execution=False,
        automatic_ledger_write=False,
        proposed_updates_only=True,
        requires_human_review=True,
    )


def copy_fake_pod_return_fixture(
    *,
    return_id: str,
    source_dir: Path,
    target_dir: Path,
) -> FakePodReturnFixtureReport:
    """Copy a direct-file fake pod return fixture into replay workspace."""

    copied: list[TransferFileRecord] = []
    omitted: list[TransferOmittedFile] = []
    errors: list[str] = []
    if not source_dir.exists() or not source_dir.is_dir():
        return FakePodReturnFixtureReport(
            return_id=return_id,
            source_dir=source_dir.as_posix(),
            target_dir=target_dir.as_posix(),
            errors=["fake pod return fixture source is missing"],
        )

    target_dir.mkdir(parents=True, exist_ok=True)
    for source_path in sorted(path for path in source_dir.iterdir() if path.is_file()):
        relative = normalize_pack_entry(source_path.relative_to(source_dir))
        warnings = transfer_warnings_for_path(relative, file_size=source_path.stat().st_size)
        if warnings:
            omitted.append(
                TransferOmittedFile(
                    path=relative,
                    reason="omitted by fake return safety policy",
                    warnings=warnings,
                )
            )
            continue
        target_path = target_dir / relative
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
            copied.append(
                TransferFileRecord(
                    path=relative,
                    sha256=sha256_file(target_path),
                    size_bytes=target_path.stat().st_size,
                    source_path=source_path.as_posix(),
                    target_path=target_path.as_posix(),
                    transferred=True,
                )
            )
        except OSError as exc:
            errors.append(f"failed to copy fake return file {relative}: {exc}")

    return FakePodReturnFixtureReport(
        return_id=return_id,
        source_dir=source_dir.as_posix(),
        target_dir=target_dir.as_posix(),
        copied_files=copied,
        omitted_files=omitted,
        errors=errors,
        live_ssh_enabled=False,
        remote_command_execution=False,
        contains_secrets=False,
        contains_raw_data=False,
        contains_model_payloads=False,
        requires_human_review=True,
    )


def render_pod_workflow_replay_report(report: PodWorkflowReplayReport) -> str:
    """Render a concise review report for the replay chain."""

    lines = [
        f"# Pod Workflow Replay Report: {report.replay_id}",
        "",
        f"- Status: `{report.status}`",
        f"- Release blocker: `{str(report.release_blocker).lower()}`",
        "- Live SSH enabled: `false`",
        "- Live network enabled: `false`",
        "- Remote command execution: `false`",
        "- Automatic Evidence Ledger write: `false`",
        "- Proposed updates only: `true`",
        "- Requires human review: `true`",
        "",
        "## Replay Chain",
        "",
    ]
    lines.extend([f"{index}. {stage}" for index, stage in enumerate(report.chain, start=1)])
    lines.extend(
        [
            "",
            "## Stage Status",
            "",
            f"- Preflight: `{report.preflight.status}`",
            f"- Context pack: `{report.context_pack.status}`",
            f"- Fake transfer: `{report.transfer.status}`",
            f"- Fake return copied files: `{len(report.fake_return.copied_files)}`",
            f"- Return verifier: `{report.return_verifier.status}`",
            "",
            "## Proposed Evidence Updates",
            "",
        ]
    )
    lines.extend(
        [
            f"- `{item.update_id}` status `{item.status}`"
            for item in report.proposed_evidence_update_report.updates
        ]
        or ["- None."]
    )
    lines.extend(
        [
            "",
            "## Safety Boundaries",
            "",
            "- No live SSH is opened.",
            "- No remote command is executed.",
            "- No Evidence Ledger entry is written automatically.",
            "- Fake/demo returns remain proposed-only until human review.",
            "- Secret, raw-data, and restricted model payload paths stay blocked.",
        ]
    )
    return "\n".join(lines) + "\n"


def _overall_status(
    preflight: SessionPreflightReport,
    context_pack: ContextPackManifest,
    transfer: TransferReport,
    fake_return: FakePodReturnFixtureReport,
    verifier: ReturnVerifierReport,
) -> PodWorkflowReplayStatus:
    if (
        preflight.status == SessionPreflightStatus.BLOCKED
        or context_pack.release_blocker
        or transfer.release_blocker
        or fake_return.release_blocker
        or verifier.release_blocker
    ):
        return PodWorkflowReplayStatus.BLOCKED
    if (
        preflight.status == SessionPreflightStatus.PASS_WITH_WARNINGS
        or context_pack.omitted_files
        or transfer.omitted_files
        or fake_return.omitted_files
    ):
        return PodWorkflowReplayStatus.PASS_WITH_WARNINGS
    return PodWorkflowReplayStatus.PASS
