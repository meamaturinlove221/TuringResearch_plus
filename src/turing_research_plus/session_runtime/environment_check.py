"""Environment checks for local session preflight."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_lifecycle import build_platform_compatibility_report
from turing_research_plus.pod_lifecycle.transfer_policy import (
    has_shell_metacharacter_risk,
    transfer_warnings_for_path,
)
from turing_research_plus.session_runtime.models import (
    SessionEnvironmentCheck,
    SessionLookupRecord,
    SessionPreflightRequest,
    SessionPreflightStatus,
)


def run_session_environment_checks(
    request: SessionPreflightRequest,
    lookup: SessionLookupRecord,
) -> list[SessionEnvironmentCheck]:
    """Run local environment checks without creating files."""

    checks: list[SessionEnvironmentCheck] = []
    project_root = Path(lookup.project_root)
    context_source = Path(lookup.context_source)
    output_dir = Path(lookup.output_dir)

    checks.append(_project_root_check(project_root))
    checks.append(_context_source_check(context_source))
    checks.append(_output_dir_check(project_root, output_dir))
    checks.extend(_identifier_shell_checks(request))
    checks.append(_memory_policy_check(request))
    checks.append(_remote_execution_disabled_check(request))
    checks.extend(_context_path_checks(lookup.context_files, allow_raw_data=request.allow_raw_data))

    compatibility = build_platform_compatibility_report(
        source_platform=request.source_platform,
        target_platform=request.target_platform,
        archive_format=request.archive_format,
    )
    if compatibility.release_blocker:
        checks.append(
            SessionEnvironmentCheck(
                check_id="platform-compatibility",
                status=SessionPreflightStatus.BLOCKED,
                message="platform compatibility requires review before unpack",
                release_blocker=True,
            )
        )
    else:
        message = "platform compatibility checked"
        if compatibility.warnings:
            message += f": {', '.join(compatibility.warnings)}"
        checks.append(
            SessionEnvironmentCheck(
                check_id="platform-compatibility",
                status=SessionPreflightStatus.PASS_WITH_WARNINGS
                if compatibility.warnings
                else SessionPreflightStatus.PASS,
                message=message,
            )
        )

    return checks


def _project_root_check(project_root: Path) -> SessionEnvironmentCheck:
    if project_root.exists() and project_root.is_dir():
        return SessionEnvironmentCheck(
            check_id="project-root-exists",
            status=SessionPreflightStatus.PASS,
            message="project root exists",
            path=project_root.as_posix(),
        )
    return SessionEnvironmentCheck(
        check_id="project-root-exists",
        status=SessionPreflightStatus.BLOCKED,
        message="project root is missing or not a directory",
        path=project_root.as_posix(),
        release_blocker=True,
    )


def _context_source_check(context_source: Path) -> SessionEnvironmentCheck:
    if context_source.exists():
        return SessionEnvironmentCheck(
            check_id="context-source-exists",
            status=SessionPreflightStatus.PASS,
            message="context source exists",
            path=context_source.as_posix(),
        )
    return SessionEnvironmentCheck(
        check_id="context-source-exists",
        status=SessionPreflightStatus.BLOCKED,
        message="context source is missing",
        path=context_source.as_posix(),
        release_blocker=True,
    )


def _output_dir_check(project_root: Path, output_dir: Path) -> SessionEnvironmentCheck:
    try:
        output_dir.relative_to(project_root)
    except ValueError:
        return SessionEnvironmentCheck(
            check_id="output-directory-safe",
            status=SessionPreflightStatus.BLOCKED,
            message="output directory must stay under project root",
            path=output_dir.as_posix(),
            release_blocker=True,
        )

    warnings = transfer_warnings_for_path(output_dir.relative_to(project_root).as_posix())
    if warnings:
        return SessionEnvironmentCheck(
            check_id="output-directory-safe",
            status=SessionPreflightStatus.BLOCKED,
            message=f"output directory path is unsafe: {', '.join(warnings)}",
            path=output_dir.as_posix(),
            release_blocker=True,
        )
    return SessionEnvironmentCheck(
        check_id="output-directory-safe",
        status=SessionPreflightStatus.PASS,
        message="output directory path is safe",
        path=output_dir.as_posix(),
    )


def _identifier_shell_checks(
    request: SessionPreflightRequest,
) -> list[SessionEnvironmentCheck]:
    checks: list[SessionEnvironmentCheck] = []
    identifiers = {
        "session_id": request.session_id,
        "context_package_id": request.lifecycle.context_package_id,
        "source_machine_label": request.lifecycle.source_machine_label,
        "target_environment_label": request.lifecycle.target_environment_label,
        "route_id": request.lifecycle.route_id,
    }
    for field_name, value in identifiers.items():
        if has_shell_metacharacter_risk(value):
            checks.append(
                SessionEnvironmentCheck(
                    check_id="shell-metacharacter-risk",
                    status=SessionPreflightStatus.BLOCKED,
                    message=f"{field_name} contains shell metacharacters",
                    release_blocker=True,
                )
            )
    if not checks:
        checks.append(
            SessionEnvironmentCheck(
                check_id="shell-metacharacter-risk",
                status=SessionPreflightStatus.PASS,
                message="session identifiers contain no shell metacharacters",
            )
        )
    return checks


def _memory_policy_check(request: SessionPreflightRequest) -> SessionEnvironmentCheck:
    memory = request.lifecycle.memory_policy
    if (
        memory.bidirectional_memory_sync
        or not memory.proposed_updates_only
        or not memory.review_required
    ):
        return SessionEnvironmentCheck(
            check_id="memory-policy-valid",
            status=SessionPreflightStatus.BLOCKED,
            message="memory policy violates review-only session runtime boundary",
            release_blocker=True,
        )
    return SessionEnvironmentCheck(
        check_id="memory-policy-valid",
        status=SessionPreflightStatus.PASS,
        message="memory policy is review-only and no-bidirectional-sync",
    )


def _remote_execution_disabled_check(
    request: SessionPreflightRequest,
) -> SessionEnvironmentCheck:
    transfer = request.lifecycle.transfer_policy
    enabled = [
        name
        for name, value in {
            "request.remote_execution_enabled": request.remote_execution_enabled,
            "transfer.remote_execution_allowed": transfer.remote_execution_allowed,
            "transfer.ssh_provision_allowed": transfer.ssh_provision_allowed,
            "transfer.modal_execution_allowed": transfer.modal_execution_allowed,
            "transfer.git_push_allowed": transfer.git_push_allowed,
            "transfer.shell_execution_allowed": transfer.shell_execution_allowed,
        }.items()
        if value
    ]
    if enabled:
        return SessionEnvironmentCheck(
            check_id="remote-execution-disabled",
            status=SessionPreflightStatus.BLOCKED,
            message=f"remote execution flags enabled: {', '.join(enabled)}",
            release_blocker=True,
        )
    return SessionEnvironmentCheck(
        check_id="remote-execution-disabled",
        status=SessionPreflightStatus.PASS,
        message="remote execution is disabled by default",
    )


def _context_path_checks(
    context_files: list[str],
    *,
    allow_raw_data: bool,
) -> list[SessionEnvironmentCheck]:
    checks: list[SessionEnvironmentCheck] = []
    for context_file in context_files:
        warnings = transfer_warnings_for_path(context_file)
        if allow_raw_data:
            warnings = [
                warning
                for warning in warnings
                if warning != "forbidden-private-or-raw-path"
            ]
        if warnings:
            checks.append(
                SessionEnvironmentCheck(
                    check_id="context-file-safe",
                    status=SessionPreflightStatus.BLOCKED,
                    message=f"context file path is unsafe: {', '.join(warnings)}",
                    path=context_file,
                    release_blocker=True,
                )
            )
    if not checks:
        checks.append(
            SessionEnvironmentCheck(
                check_id="context-file-safe",
                status=SessionPreflightStatus.PASS,
                message="context file paths are safe",
            )
        )
    return checks
