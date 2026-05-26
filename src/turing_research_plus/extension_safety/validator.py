"""Extension safety validation."""

from __future__ import annotations

from turing_research_plus.extension_safety.models import (
    ExtensionManifestRef,
    ExtensionRiskLevel,
    ExtensionSafetyFinding,
    ExtensionSafetyReport,
    ExtensionSafetyStatus,
)
from turing_research_plus.extension_safety.permission_policy import evaluate_permissions


def validate_extension_safety(manifest: ExtensionManifestRef) -> ExtensionSafetyReport:
    """Validate an extension manifest reference without loading extension code."""

    decisions = evaluate_permissions(manifest.requested_permissions)
    findings: list[ExtensionSafetyFinding] = []

    if not manifest.has_manifest:
        findings.append(
            ExtensionSafetyFinding(
                severity=ExtensionRiskLevel.CRITICAL,
                message="extension requires a manifest",
                release_blocker=True,
            )
        )
    if not manifest.has_safety_report:
        findings.append(
            ExtensionSafetyFinding(
                severity=ExtensionRiskLevel.HIGH,
                message="extension requires a safety report",
                release_blocker=False,
            )
        )
    if manifest.third_party and manifest.default_enabled:
        findings.append(
            ExtensionSafetyFinding(
                severity=ExtensionRiskLevel.CRITICAL,
                message="third-party extension must be disabled by default",
                release_blocker=True,
            )
        )
    if manifest.touches_secrets:
        findings.append(
            ExtensionSafetyFinding(
                severity=ExtensionRiskLevel.CRITICAL,
                message="secrets access is forbidden",
                release_blocker=True,
            )
        )
    if manifest.touches_raw_data:
        findings.append(
            ExtensionSafetyFinding(
                severity=ExtensionRiskLevel.HIGH,
                message="raw data access is restricted",
                release_blocker=True,
            )
        )

    for decision in decisions:
        if not decision.allowed:
            findings.append(
                ExtensionSafetyFinding(
                    severity=decision.risk_level,
                    message=decision.reason,
                    permission=decision.permission,
                    release_blocker=decision.status == ExtensionSafetyStatus.FORBIDDEN,
                )
            )

    release_blocker = any(finding.release_blocker for finding in findings)
    if release_blocker:
        status = ExtensionSafetyStatus.FORBIDDEN
    elif any(decision.status == ExtensionSafetyStatus.RESTRICTED for decision in decisions):
        status = ExtensionSafetyStatus.RESTRICTED
    elif manifest.third_party:
        status = ExtensionSafetyStatus.DISABLED_BY_DEFAULT
    else:
        status = ExtensionSafetyStatus.ALLOW_WITH_REVIEW

    return ExtensionSafetyReport(
        extension_id=manifest.extension_id,
        kind=manifest.kind,
        valid=not release_blocker,
        status=status,
        decisions=decisions,
        findings=findings,
        release_blocker=release_blocker,
        requires_human_review=True,
        executes_extension_code=False,
        loads_third_party_code=False,
    )
