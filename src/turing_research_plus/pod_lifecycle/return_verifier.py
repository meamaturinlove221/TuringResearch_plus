"""Return verification for pod context lifecycle outputs."""

from __future__ import annotations

from collections.abc import Iterable, Mapping

from turing_research_plus.pod_lifecycle.models import (
    PodContextLifecycle,
    PodLifecycleFinding,
    PodLifecycleFindingSeverity,
    PodLifecycleSafetyReport,
    PodLifecycleStatus,
)


def verify_pod_context_return(
    lifecycle: PodContextLifecycle,
    returned_files: Iterable[str],
    *,
    return_metadata: Mapping[str, object] | None = None,
) -> PodLifecycleSafetyReport:
    """Verify returned pod outputs without applying them."""

    returned = set(returned_files)
    metadata = dict(return_metadata or {})
    findings: list[PodLifecycleFinding] = []
    missing_files = [
        filename
        for filename in lifecycle.return_verification.required_files
        if filename not in returned
    ]
    for filename in missing_files:
        findings.append(
            PodLifecycleFinding(
                finding_id="missing-return-file",
                severity=PodLifecycleFindingSeverity.BLOCKER,
                message=f"required pod return file is missing: {filename}",
                path=filename,
                release_blocker=True,
            )
        )

    missing_metadata = [
        field
        for field in lifecycle.return_verification.required_metadata_fields
        if field not in metadata
    ]
    for field in missing_metadata:
        findings.append(
            PodLifecycleFinding(
                finding_id="missing-return-metadata",
                severity=PodLifecycleFindingSeverity.BLOCKER,
                message=f"required return metadata is missing: {field}",
                release_blocker=True,
            )
        )

    _validate_metadata_value(
        findings,
        field="context_package_id",
        expected=lifecycle.context_package_id,
        metadata=metadata,
    )
    _validate_metadata_value(
        findings,
        field="route_id",
        expected=lifecycle.route_id,
        metadata=metadata,
    )
    _validate_metadata_value(
        findings,
        field="target_environment_label",
        expected=lifecycle.target_environment_label,
        metadata=metadata,
    )

    return PodLifecycleSafetyReport(
        context_package_id=lifecycle.context_package_id,
        route_id=lifecycle.route_id,
        status=_status(findings),
        findings=findings,
        checked_paths=sorted(returned),
        missing_return_files=missing_files,
        missing_metadata_fields=missing_metadata,
        proposed_updates_only=True,
        requires_human_review=True,
    )


def _validate_metadata_value(
    findings: list[PodLifecycleFinding],
    *,
    field: str,
    expected: str,
    metadata: Mapping[str, object],
) -> None:
    if field not in metadata:
        return
    actual = str(metadata[field])
    if actual != expected:
        findings.append(
            PodLifecycleFinding(
                finding_id="return-metadata-mismatch",
                severity=PodLifecycleFindingSeverity.BLOCKER,
                message=f"{field} mismatch: expected {expected}, got {actual}",
                release_blocker=True,
            )
        )


def _status(findings: list[PodLifecycleFinding]) -> PodLifecycleStatus:
    if any(finding.release_blocker for finding in findings):
        return PodLifecycleStatus.BLOCKED
    if findings:
        return PodLifecycleStatus.PASS_WITH_WARNINGS
    return PodLifecycleStatus.PASS
