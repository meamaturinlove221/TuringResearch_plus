"""Markdown helpers for pod lifecycle safety reports."""

from __future__ import annotations

from turing_research_plus.pod_lifecycle.models import (
    PodLifecycleFinding,
    PodLifecycleFindingSeverity,
    PodLifecycleSafetyReport,
    PodLifecycleStatus,
)


def render_pod_lifecycle_safety_report(report: PodLifecycleSafetyReport) -> str:
    """Render a pod lifecycle safety report."""

    return report.to_markdown()


def merge_pod_lifecycle_reports(
    *reports: PodLifecycleSafetyReport,
) -> PodLifecycleSafetyReport:
    """Merge multiple pod lifecycle reports into one review surface."""

    if not reports:
        raise ValueError("at least one report is required")
    first = reports[0]
    findings: list[PodLifecycleFinding] = []
    checked_paths: list[str] = []
    missing_return_files: list[str] = []
    missing_metadata_fields: list[str] = []
    for report in reports:
        findings.extend(report.findings)
        checked_paths.extend(report.checked_paths)
        missing_return_files.extend(report.missing_return_files)
        missing_metadata_fields.extend(report.missing_metadata_fields)
    merged_findings = list({finding.model_dump_json(): finding for finding in findings}.values())
    status = PodLifecycleStatus.PASS
    if any(finding.release_blocker for finding in merged_findings):
        status = PodLifecycleStatus.BLOCKED
    elif any(finding.severity != PodLifecycleFindingSeverity.INFO for finding in merged_findings):
        status = PodLifecycleStatus.PASS_WITH_WARNINGS
    return PodLifecycleSafetyReport(
        context_package_id=first.context_package_id,
        route_id=first.route_id,
        status=status,
        findings=merged_findings,
        checked_paths=sorted(set(checked_paths)),
        missing_return_files=sorted(set(missing_return_files)),
        missing_metadata_fields=sorted(set(missing_metadata_fields)),
        proposed_updates_only=True,
        requires_human_review=True,
    )
