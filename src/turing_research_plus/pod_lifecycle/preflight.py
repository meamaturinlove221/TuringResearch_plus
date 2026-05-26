"""Preflight checks for pod context lifecycle packages."""

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.pod_lifecycle.models import (
    PodContextLifecycle,
    PodLifecycleFinding,
    PodLifecycleFindingSeverity,
    PodLifecycleSafetyReport,
    PodLifecycleStatus,
    PodPreflightCheck,
)
from turing_research_plus.pod_lifecycle.transfer_policy import (
    transfer_warnings_for_path,
    validate_transfer_policy,
)

SECRET_VALUE_PATTERN = re.compile(
    r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token|secret|password)\s*[:=]\s*"
    r"['\"]?[A-Za-z0-9][A-Za-z0-9_\-]{11,}"
)


def run_pod_context_preflight(
    lifecycle: PodContextLifecycle,
    *,
    candidate_paths: list[str | Path] | None = None,
    context_text: str = "",
) -> PodLifecycleSafetyReport:
    """Run review-only preflight checks for a pod context package."""

    transfer_report = validate_transfer_policy(lifecycle, candidate_paths=candidate_paths)
    findings = list(transfer_report.findings)
    checked_paths = list(transfer_report.checked_paths)

    if SECRET_VALUE_PATTERN.search(context_text):
        findings.append(
            PodLifecycleFinding(
                finding_id="possible-secret-value",
                severity=PodLifecycleFindingSeverity.BLOCKER,
                message="context text contains a secret-like assignment",
                release_blocker=True,
            )
        )

    lower_text = context_text.lower()
    for marker in (".env", "local_project_links.yaml", "raw data", "private_data"):
        if marker in lower_text:
            findings.append(
                PodLifecycleFinding(
                    finding_id=f"forbidden-context-marker:{marker}",
                    severity=PodLifecycleFindingSeverity.BLOCKER,
                    message=f"context text mentions forbidden payload marker: {marker}",
                    release_blocker=True,
                )
            )

    missing_context_files = _missing_required_context_files(candidate_paths or [])
    for filename in missing_context_files:
        findings.append(
            PodLifecycleFinding(
                finding_id="missing-durable-context-file",
                severity=PodLifecycleFindingSeverity.WARNING,
                message=f"durable context file is not present in candidate package: {filename}",
                path=filename,
            )
        )

    lifecycle.preflight_checks.clear()
    for warning_path in candidate_paths or []:
        warnings = transfer_warnings_for_path(warning_path)
        if warnings:
            lifecycle.preflight_checks.append(
                _check(
                    "candidate-path-safety",
                    PodLifecycleStatus.BLOCKED,
                    f"{warning_path}: {', '.join(warnings)}",
                    release_blocker=True,
                )
            )
    if not lifecycle.preflight_checks:
        lifecycle.preflight_checks.append(
            _check("candidate-path-safety", PodLifecycleStatus.PASS, "candidate paths safe")
        )

    return PodLifecycleSafetyReport(
        context_package_id=lifecycle.context_package_id,
        route_id=lifecycle.route_id,
        status=_status(findings),
        findings=findings,
        checked_paths=checked_paths,
        proposed_updates_only=True,
        requires_human_review=True,
    )


def _missing_required_context_files(paths: list[str | Path]) -> list[str]:
    if not paths:
        return []
    names = {Path(str(path).replace("\\", "/")).name for path in paths}
    required = {"PROJECT_CONTEXT.md", "MEMORY.md", "ROUTE_SPEC.yaml"}
    return sorted(required - names)


def _check(
    check_id: str,
    status: PodLifecycleStatus,
    message: str,
    *,
    release_blocker: bool = False,
) -> PodPreflightCheck:
    return PodPreflightCheck(
        check_id=check_id,
        status=status,
        message=message,
        release_blocker=release_blocker,
    )


def _status(findings: list[PodLifecycleFinding]) -> PodLifecycleStatus:
    if any(finding.release_blocker for finding in findings):
        return PodLifecycleStatus.BLOCKED
    if findings:
        return PodLifecycleStatus.PASS_WITH_WARNINGS
    return PodLifecycleStatus.PASS
