"""Hypothesis debate checks."""

from __future__ import annotations

from tuling_research_plus.hypothesis.falsifiability import is_falsifiable
from tuling_research_plus.hypothesis.models import Hypothesis
from tuling_research_plus.stress.models import (
    FailureMode,
    Severity,
    StressTestReport,
    StressWeakness,
    max_severity,
    pass_fail_from_risk,
)


def debate_hypothesis(hypothesis: Hypothesis) -> StressTestReport:
    """Debate and stress-test a hypothesis."""

    weaknesses: list[StressWeakness] = []
    failure_modes: list[FailureMode] = []
    if not is_falsifiable(hypothesis):
        weaknesses.append(
            StressWeakness(
                weakness_id="hypothesis-unfalsifiable",
                description="Hypothesis is missing falsifiability criteria.",
                severity=Severity.HIGH,
                evidence_refs=hypothesis.evidence_refs,
            )
        )
        failure_modes.append(
            FailureMode(
                mode_id="hypothesis-failure-1",
                description="Experiment cannot disconfirm the hypothesis.",
                severity=Severity.HIGH,
                mitigation="Add falsifying observation and minimum test before promotion.",
            )
        )
    if hypothesis.risk_level == "high":
        weaknesses.append(
            StressWeakness(
                weakness_id="hypothesis-high-risk",
                description="High-risk hypothesis needs stronger boundary testing.",
                severity=Severity.MEDIUM,
                evidence_refs=hypothesis.evidence_refs,
            )
        )
    if not weaknesses:
        weaknesses.append(
            StressWeakness(
                weakness_id="hypothesis-counterargument",
                description="Alternative explanation may account for the same outcome.",
                severity=Severity.LOW,
                evidence_refs=hypothesis.evidence_refs,
            )
        )
    severity = max_severity([weakness.severity for weakness in weaknesses])
    mitigations = [
        mode.mitigation
        for mode in failure_modes
        if mode.mitigation is not None
    ]
    return StressTestReport(
        artifact_id=hypothesis.hypothesis_id,
        weaknesses=weaknesses,
        severity=severity,
        attack_paths=["Invert the mechanism and test whether the prediction still holds."],
        counterarguments=[
            "Observed change may be caused by corpus quality instead of the proposed mechanism."
        ],
        failure_modes=failure_modes,
        mitigations=mitigations,
        residual_risk=Severity.MEDIUM if mitigations else severity,
        pass_fail=pass_fail_from_risk(severity),
        rerun_recommendations=["Rerun after falsifiability and boundary criteria are tightened."],
    )
