"""Local fake/default command layer for the Session CLI surface."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_lifecycle import PodContextLifecycle
from turing_research_plus.session_runtime.cli_report import (
    SessionCLICommandReport,
    SessionCLIStatus,
    build_session_cli_surface_report,
    render_session_cli_command_report,
    write_cli_report_if_requested,
)
from turing_research_plus.session_runtime.context_pack_builder import (
    ContextPackBuildRequest,
    build_context_pack,
)
from turing_research_plus.session_runtime.models import (
    SessionPreflightRequest,
    SessionPreflightStatus,
)
from turing_research_plus.session_runtime.preflight_runner import run_session_preflight
from turing_research_plus.session_runtime.report import render_session_preflight_report
from turing_research_plus.session_runtime.return_verifier import (
    ReturnVerifierStatus,
    render_return_verifier_report,
    verify_return_package,
)
from turing_research_plus.session_runtime.transfer_report import (
    TransferMode,
    TransferStatus,
    render_transfer_report,
)
from turing_research_plus.session_runtime.transfer_runner import (
    TransferRunnerRequest,
    run_transfer,
)
from turing_research_plus.session_runtime.workflow_replay import (
    PodWorkflowReplayRequest,
    PodWorkflowReplayStatus,
    render_pod_workflow_replay_report,
    run_pod_workflow_replay,
)


def run_preflight_command(
    *,
    project_root: Path,
    context_source: Path,
    output_dir: Path,
    session_id: str = "session-cli-preflight",
    package_id: str = "ctx-cli-preflight",
    route_id: str = "route-cli-preflight",
    output: Path | None = None,
) -> SessionCLICommandReport:
    """Run local preflight and return a CLI report."""

    lifecycle = PodContextLifecycle(
        context_package_id=package_id,
        source_machine_label="local-cli-machine",
        target_environment_label="fake-cli-pod",
        route_id=route_id,
    )
    preflight = run_session_preflight(
        SessionPreflightRequest(
            session_id=session_id,
            project_root=project_root,
            context_source=context_source,
            output_dir=output_dir,
            lifecycle=lifecycle,
        )
    )
    report = SessionCLICommandReport(
        command="session preflight",
        status=_status_from_preflight(preflight.status),
        summary="Session preflight completed in local dry-run mode.",
        detail_markdown=render_session_preflight_report(preflight),
        data={
            "session_id": preflight.session_id,
            "context_package_id": preflight.context_package_id,
            "route_id": preflight.route_id,
            "remote_execution_enabled": preflight.remote_execution_enabled,
            "live_network_enabled": preflight.live_network_enabled,
        },
    )
    return write_cli_report_if_requested(report, output)


def run_pack_command(
    *,
    source_dir: Path,
    output_dir: Path,
    package_id: str = "ctx-cli-pack",
    route_id: str = "route-cli-pack",
    project_name: str = "TuringResearch Plus",
    output: Path | None = None,
) -> SessionCLICommandReport:
    """Build a safe local context pack and return a CLI report."""

    manifest = build_context_pack(
        ContextPackBuildRequest(
            package_id=package_id,
            route_id=route_id,
            source_dir=source_dir,
            output_dir=output_dir,
            project_name=project_name,
        )
    )
    detail_path = output_dir / "CONTEXT_PACK_MANIFEST.md"
    detail = detail_path.read_text(encoding="utf-8") if detail_path.exists() else ""
    report = SessionCLICommandReport(
        command="session pack",
        status=SessionCLIStatus.BLOCKED
        if manifest.release_blocker
        else (
            SessionCLIStatus.PASS_WITH_WARNINGS
            if manifest.omitted_files
            else SessionCLIStatus.PASS
        ),
        summary="Context pack build completed in local safe mode.",
        detail_markdown=detail,
        data={
            "package_id": manifest.package_id,
            "route_id": manifest.route_id,
            "included_files": len(manifest.files),
            "omitted_files": len(manifest.omitted_files),
            "output_dir": manifest.output_dir,
        },
    )
    return write_cli_report_if_requested(report, output)


def run_transfer_command(
    *,
    source_dir: Path,
    target_dir: Path,
    transfer_id: str = "transfer-cli-fake",
    package_id: str = "ctx-cli-transfer",
    fake: bool = True,
    output: Path | None = None,
) -> SessionCLICommandReport:
    """Run fake transfer and return a CLI report."""

    if not fake:
        raise ValueError("Session CLI transfer only supports --fake by default")
    transfer = run_transfer(
        TransferRunnerRequest(
            transfer_id=transfer_id,
            package_id=package_id,
            source_dir=source_dir,
            target=target_dir.as_posix(),
            mode=TransferMode.FAKE,
        )
    )
    report = SessionCLICommandReport(
        command="session transfer --fake",
        status=SessionCLIStatus.BLOCKED
        if transfer.status == TransferStatus.BLOCKED
        else SessionCLIStatus.PASS,
        summary="Fake local transfer completed without remote connection.",
        detail_markdown=render_transfer_report(transfer),
        data={
            "transfer_id": transfer.transfer_id,
            "package_id": transfer.package_id,
            "mode": transfer.mode,
            "status": transfer.status,
            "selected_files": len(transfer.selected_files),
            "omitted_files": len(transfer.omitted_files),
        },
    )
    return write_cli_report_if_requested(report, output)


def run_verify_return_command(
    *,
    return_dir: Path,
    return_id: str = "return-cli-verify",
    output: Path | None = None,
) -> SessionCLICommandReport:
    """Verify a structured return package and return a CLI report."""

    verifier = verify_return_package(return_dir, return_id=return_id)
    report = SessionCLICommandReport(
        command="session verify-return",
        status=SessionCLIStatus.BLOCKED
        if verifier.status == ReturnVerifierStatus.BLOCKED
        else SessionCLIStatus.PASS,
        summary="Return package verification completed without ledger mutation.",
        detail_markdown=render_return_verifier_report(verifier),
        data={
            "return_id": verifier.return_id,
            "missing_artifacts": len(verifier.missing_artifacts),
            "unsafe_files": len(verifier.unsafe_files),
            "checksum_mismatches": len(verifier.checksum_mismatches),
            "proposed_updates": len(verifier.proposed_updates.updates),
        },
    )
    return write_cli_report_if_requested(report, output)


def run_replay_command(
    *,
    project_root: Path,
    preflight_context_source: Path,
    preflight_output_dir: Path,
    context_pack_source_dir: Path,
    replay_workspace: Path,
    fake_return_fixture_dir: Path,
    replay_id: str = "session-cli-replay",
    session_id: str = "session-cli-replay",
    package_id: str = "ctx-cli-replay",
    route_id: str = "route-cli-replay",
    output: Path | None = None,
) -> SessionCLICommandReport:
    """Run the full fake pod workflow replay and return a CLI report."""

    replay = run_pod_workflow_replay(
        PodWorkflowReplayRequest(
            replay_id=replay_id,
            session_id=session_id,
            package_id=package_id,
            route_id=route_id,
            project_root=project_root,
            preflight_context_source=preflight_context_source,
            preflight_output_dir=preflight_output_dir,
            context_pack_source_dir=context_pack_source_dir,
            replay_workspace=replay_workspace,
            fake_return_fixture_dir=fake_return_fixture_dir,
        )
    )
    report = SessionCLICommandReport(
        command="session replay",
        status=_status_from_replay(replay.status),
        summary="Full fake pod workflow replay completed.",
        detail_markdown=render_pod_workflow_replay_report(replay),
        data={
            "replay_id": replay.replay_id,
            "chain_length": len(replay.chain),
            "proposed_updates": len(replay.proposed_evidence_update_report.updates),
        },
    )
    return write_cli_report_if_requested(report, output)


def run_report_command(*, output: Path | None = None) -> SessionCLICommandReport:
    """Return the static Session CLI surface report."""

    return write_cli_report_if_requested(build_session_cli_surface_report(), output)


def render_cli_report(report: SessionCLICommandReport) -> str:
    """Render a CLI command report."""

    return render_session_cli_command_report(report)


def _status_from_preflight(status: SessionPreflightStatus) -> SessionCLIStatus:
    if status == SessionPreflightStatus.BLOCKED:
        return SessionCLIStatus.BLOCKED
    if status == SessionPreflightStatus.PASS_WITH_WARNINGS:
        return SessionCLIStatus.PASS_WITH_WARNINGS
    return SessionCLIStatus.PASS


def _status_from_replay(status: PodWorkflowReplayStatus) -> SessionCLIStatus:
    if status == PodWorkflowReplayStatus.BLOCKED:
        return SessionCLIStatus.BLOCKED
    if status == PodWorkflowReplayStatus.PASS_WITH_WARNINGS:
        return SessionCLIStatus.PASS_WITH_WARNINGS
    return SessionCLIStatus.PASS
