"""Safety checks for dry-run repository split exports."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.privacy.models import PrivacyFindingType
from turing_research_plus.privacy.scanner import scan_privacy_paths
from turing_research_plus.repo_split.models import (
    RepoSplitFileRecord,
    RepoSplitSafetyFinding,
    RepoSplitSafetyReport,
)

PATH_BLOCKLIST = {
    ".env",
    ".env.local",
    "local_project_links.yaml",
}
BLOCKED_SUFFIXES = {
    ".npz",
    ".pkl",
    ".pt",
    ".pth",
    ".ckpt",
    ".safetensors",
    ".zip",
    ".tar",
    ".gz",
}
POLICY_MENTION_FINDINGS = {PrivacyFindingType.PRIVATE_ADVISOR_FEEDBACK}


def evaluate_split_file(
    path: Path,
    *,
    source_root: Path,
    allowed_suffixes: set[str],
    max_file_size_bytes: int,
) -> tuple[bool, list[RepoSplitSafetyFinding]]:
    """Return whether a file is safe for dry-run export and why."""

    relative = _relative_to_root(path, source_root)
    findings: list[RepoSplitSafetyFinding] = []

    if not _is_under_root(path, source_root):
        findings.append(
            RepoSplitSafetyFinding(
                relative_path=relative,
                finding_type="outside-source-root",
                severity="blocker",
                message="File is outside the split source root.",
                release_blocker=True,
            )
        )
    if path.name in PATH_BLOCKLIST:
        findings.append(
            RepoSplitSafetyFinding(
                relative_path=relative,
                finding_type="blocked-filename",
                severity="blocker",
                message="Filename is forbidden in public split exports.",
                release_blocker=True,
            )
        )
    if path.suffix.lower() in BLOCKED_SUFFIXES:
        findings.append(
            RepoSplitSafetyFinding(
                relative_path=relative,
                finding_type="blocked-suffix",
                severity="blocker",
                message="Binary/model/archive payloads are not exported by dry-run split.",
                release_blocker=True,
            )
        )
    if path.suffix.lower() not in allowed_suffixes:
        findings.append(
            RepoSplitSafetyFinding(
                relative_path=relative,
                finding_type="unsupported-suffix",
                severity="warning",
                message="Dry-run exporter only copies public-safe text-like files.",
                release_blocker=True,
            )
        )
    if path.stat().st_size > max_file_size_bytes:
        findings.append(
            RepoSplitSafetyFinding(
                relative_path=relative,
                finding_type="file-too-large",
                severity="blocker",
                message="File exceeds dry-run split size limit.",
                release_blocker=True,
            )
        )

    privacy = scan_privacy_paths([path])
    for finding in privacy.findings:
        if finding.finding_type in POLICY_MENTION_FINDINGS and not finding.release_blocker:
            findings.append(
                RepoSplitSafetyFinding(
                    relative_path=relative,
                    finding_type=f"policy-mention:{finding.finding_type.value}",
                    severity=finding.severity.value,
                    message="Safety policy text mentions an excluded private item.",
                    release_blocker=False,
                )
            )
            continue
        findings.append(
            RepoSplitSafetyFinding(
                relative_path=relative,
                finding_type=f"privacy:{finding.finding_type.value}",
                severity=finding.severity.value,
                message=finding.message,
                release_blocker=True,
            )
        )

    return not any(finding.release_blocker for finding in findings), findings


def build_safety_report(
    *,
    candidate_id: str,
    checked_files: list[str],
    findings: list[RepoSplitSafetyFinding],
    omitted_files: list[RepoSplitFileRecord],
) -> RepoSplitSafetyReport:
    """Build a safety report with standard dry-run limitations."""

    return RepoSplitSafetyReport(
        candidate_id=candidate_id,
        checked_files=checked_files,
        findings=findings,
        omitted_files=omitted_files,
        requires_human_review=True,
        limitations=[
            "Dry-run export does not create repositories.",
            "Dry-run export does not push git remotes.",
            "Safety checks are pattern based and require human review.",
            "Public split candidates must still pass privacy and compliance review.",
        ],
    )


def render_safety_report(report: RepoSplitSafetyReport) -> str:
    """Render split safety report as Markdown."""

    lines = [
        f"# Split Safety Report: {report.candidate_id}",
        "",
        f"- safe_to_export: `{str(report.safe_to_export).lower()}`",
        f"- release_blocker: `{str(report.release_blocker).lower()}`",
        "- requires_human_review: `true`",
        "",
        "## Checked Files",
        "",
    ]
    lines.extend([f"- `{item}`" for item in report.checked_files] or ["- none"])
    lines.extend(["", "## Omitted Files", ""])
    if report.omitted_files:
        lines.extend(
            [
                f"- `{item.relative_path}`: {item.omitted_reason}"
                for item in report.omitted_files
            ]
        )
    else:
        lines.append("- none")
    lines.extend(["", "## Findings", ""])
    if report.findings:
        lines.extend(
            [
                f"- `{finding.severity}` `{finding.finding_type}` "
                f"`{finding.relative_path}`: {finding.message}"
                for finding in report.findings
            ]
        )
    else:
        lines.append("- none")
    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {item}" for item in report.limitations])
    lines.append("")
    return "\n".join(lines)


def _is_under_root(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name
