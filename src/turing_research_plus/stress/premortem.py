"""Experiment premortem checks."""

from __future__ import annotations

from tuling_research_plus.stress.models import (
    ExperimentPlan,
    FailureMode,
    Severity,
    StressTestReport,
    StressWeakness,
    max_severity,
    pass_fail_from_risk,
)


def experiment_premortem(plan: ExperimentPlan) -> StressTestReport:
    """Reject weak experiment plans and report failure modes."""

    weaknesses: list[StressWeakness] = []
    failure_modes: list[FailureMode] = []
    if not plan.required_data:
        weaknesses.append(
            StressWeakness(
                weakness_id="experiment-missing-data",
                description="Experiment plan does not specify required data.",
                severity=Severity.HIGH,
                evidence_refs=plan.evidence_refs,
            )
        )
    if not plan.metrics:
        weaknesses.append(
            StressWeakness(
                weakness_id="experiment-missing-metrics",
                description="Experiment plan does not specify measurement metrics.",
                severity=Severity.HIGH,
                evidence_refs=plan.evidence_refs,
            )
        )
    if not plan.controls:
        weaknesses.append(
            StressWeakness(
                weakness_id="experiment-missing-controls",
                description="Experiment plan has no control variables or baseline.",
                severity=Severity.MEDIUM,
                evidence_refs=plan.evidence_refs,
            )
        )
    if not plan.success_criteria:
        weaknesses.append(
            StressWeakness(
                weakness_id="experiment-missing-success-criteria",
                description="Experiment plan has no success criteria.",
                severity=Severity.HIGH,
                evidence_refs=plan.evidence_refs,
            )
        )
    if weaknesses:
        failure_modes.append(
            FailureMode(
                mode_id="experiment-failure-1",
                description="Weak plan could produce uninterpretable results.",
                severity=max_severity([weakness.severity for weakness in weaknesses]),
                mitigation="Add data, metrics, controls, and success criteria before execution.",
            )
        )
    else:
        weaknesses.append(
            StressWeakness(
                weakness_id="experiment-resource-risk",
                description="Execution may still be constrained by resource availability.",
                severity=Severity.LOW,
                evidence_refs=plan.evidence_refs,
            )
        )
    severity = max_severity([weakness.severity for weakness in weaknesses])
    mitigations = [
        mode.mitigation
        for mode in failure_modes
        if mode.mitigation is not None
    ]
    return StressTestReport(
        artifact_id=plan.plan_id,
        weaknesses=weaknesses,
        severity=severity,
        attack_paths=["Remove controls or metrics and inspect whether conclusions collapse."],
        counterarguments=["A weak plan can be useful for scoping, but not for execution."],
        failure_modes=failure_modes,
        mitigations=mitigations,
        residual_risk=Severity.MEDIUM if mitigations else severity,
        pass_fail=pass_fail_from_risk(severity),
        rerun_recommendations=["Rerun premortem after plan fields are completed."],
    )
