"""Transfer policy checks for pod context lifecycle packages."""

from __future__ import annotations

import re
from pathlib import Path

from turing_research_plus.pod_lifecycle.models import (
    PodContextLifecycle,
    PodLifecycleFinding,
    PodLifecycleFindingSeverity,
    PodLifecycleSafetyReport,
    PodLifecycleStatus,
)

SHELL_META_PATTERN = re.compile(r"[;&|`$<>]")
SECRET_NAME_PATTERN = re.compile(r"(?i)(api[_-]?key|token|secret|password)")
PRIVATE_DRIVE_PATTERN = re.compile(r"(?i)^[a-z]:[\\/]")

FORBIDDEN_DOTFILES = {
    ".env",
    ".git",
    ".ssh",
    ".codex",
    ".aws",
    ".azure",
    ".config",
}
FORBIDDEN_PARTS = {
    "private_data",
    "raw_data",
    "raw_dataset",
    "datasets",
    "secrets",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def transfer_warnings_for_path(
    path: str | Path,
    *,
    file_size: int | None = None,
    max_npz_size: int = 5_000_000,
) -> list[str]:
    """Return transfer warnings for one archive or package path."""

    raw = str(path).replace("\\", "/")
    candidate = Path(raw)
    lower_parts = {part.lower() for part in candidate.parts}
    lower_name = candidate.name.lower()
    warnings: list[str] = []

    if raw.startswith("/") or PRIVATE_DRIVE_PATTERN.match(raw):
        warnings.append("unsafe-archive-absolute-path")
    if ".." in candidate.parts or raw.startswith("../") or "/../" in raw:
        warnings.append("unsafe-archive-path-traversal")
    if SHELL_META_PATTERN.search(raw):
        warnings.append("shell-metacharacter-risk")
    if lower_parts & FORBIDDEN_DOTFILES or lower_name in FORBIDDEN_DOTFILES:
        warnings.append("forbidden-dotfile")
    if lower_name.endswith(".env"):
        warnings.append("forbidden-env-file")
    if "local_project_links.yaml" == lower_name:
        warnings.append("forbidden-local-project-links")
    if lower_parts & FORBIDDEN_PARTS:
        warnings.append("forbidden-private-or-raw-path")
    if SECRET_NAME_PATTERN.search(raw):
        warnings.append("forbidden-secret-like-path")
    body_model_prefix = "smpl" + "x_"
    if lower_name.startswith(body_model_prefix) and candidate.suffix.lower() in {".npz", ".pkl"}:
        warnings.append("forbidden-body-model-file")
    if "smpl-x" in lower_name and candidate.suffix.lower() in {".npz", ".pkl"}:
        warnings.append("forbidden-body-model-file")
    if lower_name == "predictions.npz":
        warnings.append("summary-only-npz-required")
    if candidate.suffix.lower() == ".npz" and file_size is not None and file_size > max_npz_size:
        warnings.append("huge-npz-forbidden")
    return list(dict.fromkeys(warnings))


def has_shell_metacharacter_risk(value: str) -> bool:
    """Return whether a lifecycle identifier contains shell metacharacters."""

    return bool(SHELL_META_PATTERN.search(value))


def validate_transfer_policy(
    lifecycle: PodContextLifecycle,
    *,
    candidate_paths: list[str | Path] | None = None,
) -> PodLifecycleSafetyReport:
    """Validate transfer policy and candidate archive paths."""

    findings: list[PodLifecycleFinding] = []

    for field_name, value in {
        "context_package_id": lifecycle.context_package_id,
        "source_machine_label": lifecycle.source_machine_label,
        "target_environment_label": lifecycle.target_environment_label,
        "route_id": lifecycle.route_id,
    }.items():
        if has_shell_metacharacter_risk(value):
            findings.append(
                PodLifecycleFinding(
                    finding_id="shell-metacharacter-risk",
                    severity=PodLifecycleFindingSeverity.BLOCKER,
                    message=f"{field_name} contains shell metacharacters",
                    release_blocker=True,
                )
            )

    if lifecycle.transfer_policy.transport != "git_context_package":
        findings.append(
            PodLifecycleFinding(
                finding_id="unexpected-transport",
                severity=PodLifecycleFindingSeverity.WARNING,
                message="v1.0 lifecycle expects git_context_package transport only",
            )
        )

    checked_paths: list[str] = []
    for path in candidate_paths or []:
        checked_paths.append(str(path))
        for warning in transfer_warnings_for_path(path):
            findings.append(
                PodLifecycleFinding(
                    finding_id=warning,
                    severity=PodLifecycleFindingSeverity.BLOCKER,
                    message=f"path is unsafe for pod context transfer: {warning}",
                    path=str(path),
                    release_blocker=True,
                )
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


def _status(findings: list[PodLifecycleFinding]) -> PodLifecycleStatus:
    if any(finding.release_blocker for finding in findings):
        return PodLifecycleStatus.BLOCKED
    if findings:
        return PodLifecycleStatus.PASS_WITH_WARNINGS
    return PodLifecycleStatus.PASS
