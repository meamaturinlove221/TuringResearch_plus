"""Dry-run exporter for future repository split candidates."""

from __future__ import annotations

import shutil
from pathlib import Path

from turing_research_plus.repo_split.manifest import sha256_file, split_manifest_to_yaml
from turing_research_plus.repo_split.models import (
    RepoSplitDryRunRequest,
    RepoSplitDryRunResult,
    RepoSplitFileRecord,
    RepoSplitManifest,
    RepoSplitSafetyFinding,
    RepoSplitStatus,
)
from turing_research_plus.repo_split.safety import (
    build_safety_report,
    evaluate_split_file,
    render_safety_report,
)


def export_split_dry_run(request: RepoSplitDryRunRequest) -> RepoSplitDryRunResult:
    """Copy public-safe split candidate files to a local dry-run export directory."""

    export_dir = request.output_root / request.candidate_id
    export_dir.mkdir(parents=True, exist_ok=True)
    included: list[RepoSplitFileRecord] = []
    omitted: list[RepoSplitFileRecord] = []
    all_findings = []

    file_paths = request.file_paths or collect_split_candidate_files(request.source_root)
    checked_files: list[str] = []
    for relative_path in file_paths:
        source_path = (
            relative_path if relative_path.is_absolute() else request.source_root / relative_path
        )
        relative = _relative_to_root(source_path, request.source_root)
        checked_files.append(relative)
        if not source_path.exists() or not source_path.is_file():
            omitted.append(
                RepoSplitFileRecord(
                    relative_path=relative,
                    included=False,
                    omitted_reason="source file missing",
                    safety_warnings=["missing"],
                )
            )
            continue

        safe, findings = evaluate_split_file(
            source_path,
            source_root=request.source_root,
            allowed_suffixes=request.allowed_suffixes,
            max_file_size_bytes=request.max_file_size_bytes,
        )
        all_findings.extend(findings)
        if not safe:
            omitted.append(
                RepoSplitFileRecord(
                    relative_path=relative,
                    included=False,
                    file_size=source_path.stat().st_size,
                    sha256=sha256_file(source_path),
                    omitted_reason=_omitted_reason(findings),
                    safety_warnings=[finding.finding_type for finding in findings],
                )
            )
            continue

        destination = export_dir / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        included.append(
            RepoSplitFileRecord(
                relative_path=relative,
                included=True,
                file_size=destination.stat().st_size,
                sha256=sha256_file(destination),
                safety_warnings=[
                    finding.finding_type for finding in findings if not finding.release_blocker
                ],
            )
        )

    safety_report = build_safety_report(
        candidate_id=request.candidate_id,
        checked_files=checked_files,
        findings=all_findings,
        omitted_files=omitted,
    )
    manifest = RepoSplitManifest(
        candidate_id=request.candidate_id,
        source_root=_safe_source_root_label(request.source_root),
        included_files=included,
        omitted_files=omitted,
        safety_report_path="safety_report.md",
        requires_human_review=True,
    )
    (export_dir / "split_manifest.yaml").write_text(
        split_manifest_to_yaml(manifest),
        encoding="utf-8",
    )
    (export_dir / "safety_report.md").write_text(
        render_safety_report(safety_report),
        encoding="utf-8",
    )
    status = RepoSplitStatus.PASS
    if safety_report.release_blocker:
        status = RepoSplitStatus.BLOCKED
    elif all_findings or omitted:
        status = RepoSplitStatus.PASS_WITH_WARNINGS

    return RepoSplitDryRunResult(
        candidate_id=request.candidate_id,
        export_dir=export_dir,
        manifest=manifest,
        safety_report=safety_report,
        status=status,
    )


def collect_split_candidate_files(source_root: Path) -> list[Path]:
    """Collect files under a split candidate root as relative paths."""

    return sorted(
        path.relative_to(source_root)
        for path in source_root.rglob("*")
        if path.is_file()
    )


def _relative_to_root(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.name


def _safe_source_root_label(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def _omitted_reason(findings: list[RepoSplitSafetyFinding]) -> str:
    blockers = [
        getattr(finding, "finding_type", "unknown")
        for finding in findings
        if getattr(finding, "release_blocker", False)
    ]
    if blockers:
        return "blocked by split safety policy: " + ", ".join(blockers)
    return "blocked by split safety policy"
