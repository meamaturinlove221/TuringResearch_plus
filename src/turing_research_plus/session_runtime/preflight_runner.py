"""Local-only session preflight runner."""

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.pod_lifecycle import (
    build_platform_compatibility_report,
    run_pod_context_preflight,
)
from turing_research_plus.session_runtime.environment_check import (
    run_session_environment_checks,
)
from turing_research_plus.session_runtime.models import (
    SessionEnvironmentCheck,
    SessionPreflightFinding,
    SessionPreflightFindingSeverity,
    SessionPreflightReport,
    SessionPreflightRequest,
    SessionPreflightStatus,
)
from turing_research_plus.session_runtime.session_lookup import (
    build_session_lookup_record,
)

SECRET_VALUE_PATTERN = re.compile(
    r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret|password)\s*[:=]\s*"
    r"['\"]?[A-Za-z0-9][A-Za-z0-9_\-]{11,}"
)


def run_session_preflight(request: SessionPreflightRequest) -> SessionPreflightReport:
    """Run a local review-only session preflight."""

    lookup = build_session_lookup_record(request)
    environment_checks = run_session_environment_checks(request, lookup)
    context_text = _read_context_text(Path(lookup.context_source))
    pod_candidate_paths: list[str | Path] = list(lookup.context_files)
    pod_report = run_pod_context_preflight(
        request.lifecycle,
        candidate_paths=pod_candidate_paths,
        context_text=context_text,
    )
    platform = build_platform_compatibility_report(
        source_platform=request.source_platform,
        target_platform=request.target_platform,
        archive_format=request.archive_format,
    )

    findings = [
        SessionPreflightFinding(
            finding_id=finding.finding_id,
            severity=_severity_from_pod(finding.release_blocker),
            message=finding.message,
            path=finding.path,
            release_blocker=finding.release_blocker,
        )
        for finding in pod_report.findings
    ]
    findings.extend(_secret_findings(context_text))
    status = _status(environment_checks, findings)

    return SessionPreflightReport(
        session_id=request.session_id,
        context_package_id=request.lifecycle.context_package_id,
        route_id=request.lifecycle.route_id,
        status=status,
        lookup=lookup,
        environment_checks=environment_checks,
        findings=findings,
        checked_paths=lookup.context_files,
        platform_warnings=platform.warnings,
        remote_execution_enabled=False,
        live_network_enabled=False,
        proposed_updates_only=True,
        requires_human_review=True,
    )


def _read_context_text(context_source: Path, *, max_bytes: int = 100_000) -> str:
    if not context_source.exists():
        return ""
    files = [context_source] if context_source.is_file() else sorted(context_source.rglob("*"))
    chunks: list[str] = []
    total = 0
    for path in files:
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml", ".json", ".txt"}:
            continue
        if path.stat().st_size > max_bytes:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        total += len(text.encode("utf-8"))
        if total > max_bytes:
            break
        chunks.append(text)
    return "\n".join(chunks)


def _secret_findings(context_text: str) -> list[SessionPreflightFinding]:
    if not SECRET_VALUE_PATTERN.search(context_text):
        return []
    return [
        SessionPreflightFinding(
            finding_id="possible-secret-value",
            severity=SessionPreflightFindingSeverity.BLOCKER,
            message="context source contains a secret-like assignment",
            release_blocker=True,
        )
    ]


def _severity_from_pod(release_blocker: bool) -> SessionPreflightFindingSeverity:
    return (
        SessionPreflightFindingSeverity.BLOCKER
        if release_blocker
        else SessionPreflightFindingSeverity.WARNING
    )


def _status(
    checks: list[SessionEnvironmentCheck],
    findings: list[SessionPreflightFinding],
) -> SessionPreflightStatus:
    if any(check.release_blocker for check in checks) or any(
        finding.release_blocker for finding in findings
    ):
        return SessionPreflightStatus.BLOCKED
    if (
        any(check.status == SessionPreflightStatus.PASS_WITH_WARNINGS for check in checks)
        or findings
    ):
        return SessionPreflightStatus.PASS_WITH_WARNINGS
    return SessionPreflightStatus.PASS
