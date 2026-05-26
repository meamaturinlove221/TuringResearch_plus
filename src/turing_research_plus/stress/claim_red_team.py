"""Claim red-team checks."""

from __future__ import annotations

from tuling_research_plus.stress.models import (
    Claim,
    FailureMode,
    Severity,
    StressTestReport,
    StressWeakness,
    max_severity,
    pass_fail_from_risk,
)


def red_team_claim(claim: Claim) -> StressTestReport:
    """Flag unsupported or weak claims."""

    weaknesses: list[StressWeakness] = []
    failure_modes: list[FailureMode] = []
    if not claim.evidence_refs:
        weaknesses.append(
            StressWeakness(
                weakness_id="claim-unsupported",
                description="Unsupported claim has no EvidenceRef.",
                severity=Severity.HIGH,
            )
        )
        failure_modes.append(
            FailureMode(
                mode_id="claim-failure-1",
                description="Downstream synthesis may treat unsupported text as fact.",
                severity=Severity.HIGH,
                mitigation="Attach source-backed EvidenceRef before reuse.",
            )
        )
    else:
        weaknesses.append(
            StressWeakness(
                weakness_id="claim-scope",
                description="Claim could be overgeneralized beyond its evidence scope.",
                severity=Severity.LOW,
                evidence_refs=claim.evidence_refs,
            )
        )
    severity = max_severity([weakness.severity for weakness in weaknesses])
    mitigations = [
        mode.mitigation
        for mode in failure_modes
        if mode.mitigation is not None
    ]
    return StressTestReport(
        artifact_id=claim.claim_id,
        weaknesses=weaknesses,
        severity=severity,
        attack_paths=["Remove evidence boundary and test if claim still survives."],
        counterarguments=["The claim may still be useful as a hypothesis, not a conclusion."],
        failure_modes=failure_modes,
        mitigations=mitigations,
        residual_risk=Severity.MEDIUM if mitigations else severity,
        pass_fail=pass_fail_from_risk(severity),
        rerun_recommendations=["Rerun after evidence refs are attached."],
    )
