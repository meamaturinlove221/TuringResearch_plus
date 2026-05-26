"""Counterfactual and failure-mode probes."""

from __future__ import annotations

from tuling_research_plus.stress.models import (
    FailureMode,
    Severity,
    StressTestReport,
    StressWeakness,
    max_severity,
    pass_fail_from_risk,
)


def counterfactual_probe(
    artifact_id: str,
    claim: str,
    evidence_count: int,
    mitigated: bool = False,
) -> StressTestReport:
    """Probe a claim under a counterfactual evidence condition."""

    severity = Severity.MEDIUM if evidence_count > 0 else Severity.HIGH
    residual = Severity.LOW if mitigated else severity
    weakness = StressWeakness(
        weakness_id="counterfactual-fragility",
        description=f"Claim may fail if counterfactual holds: {claim}",
        severity=severity,
    )
    mitigation = "Add counterfactual evidence and rerun the decision."
    return StressTestReport(
        artifact_id=artifact_id,
        weaknesses=[weakness],
        severity=severity,
        attack_paths=["Assume the main evidence source is wrong or non-representative."],
        counterarguments=["The claim may survive if independent evidence agrees."],
        failure_modes=[
            FailureMode(
                mode_id="counterfactual-failure-1",
                description="Conclusion reverses under plausible alternate evidence.",
                severity=severity,
                mitigation=mitigation,
            )
        ],
        mitigations=[mitigation] if mitigated else [],
        residual_risk=residual,
        pass_fail=pass_fail_from_risk(residual),
        rerun_recommendations=["Rerun with independent evidence or a negative control."],
    )


def failure_mode_analyze(
    artifact_id: str,
    failure_modes: list[FailureMode],
    mitigations: list[str] | None = None,
) -> StressTestReport:
    """Aggregate failure modes into a stress report."""

    mitigation_list = mitigations or []
    severity = max_severity([mode.severity for mode in failure_modes])
    residual = Severity.LOW if mitigation_list else severity
    return StressTestReport(
        artifact_id=artifact_id,
        weaknesses=[
            StressWeakness(
                weakness_id=f"weakness-{index}",
                description=mode.description,
                severity=mode.severity,
            )
            for index, mode in enumerate(failure_modes, start=1)
        ],
        severity=severity,
        attack_paths=["Combine failure modes and test if recommendation still holds."],
        counterarguments=["Some failure modes may be operational rather than conceptual."],
        failure_modes=failure_modes,
        mitigations=mitigation_list,
        residual_risk=residual,
        pass_fail=pass_fail_from_risk(residual),
        rerun_recommendations=["Rerun after mitigation evidence is attached."],
    )
