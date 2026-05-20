from tuling_research_plus.stress.models import (
    FailureMode,
    PassFail,
    Severity,
    StressTestReport,
    StressWeakness,
)


def test_stress_report_contains_required_fields_and_artifact() -> None:
    report = StressTestReport(
        artifact_id="artifact-1",
        weaknesses=[
            StressWeakness(
                weakness_id="weakness-1",
                description="Unsupported boundary.",
                severity=Severity.MEDIUM,
            )
        ],
        severity=Severity.MEDIUM,
        attack_paths=["Remove evidence."],
        counterarguments=["Could survive as a hypothesis."],
        failure_modes=[
            FailureMode(
                mode_id="mode-1",
                description="Downstream synthesis fails.",
                severity=Severity.MEDIUM,
                mitigation="Attach evidence.",
            )
        ],
        mitigations=["Attach evidence."],
        residual_risk=Severity.LOW,
        pass_fail=PassFail.PASS,
        rerun_recommendations=["Rerun after mitigation."],
    )
    artifact = report.to_research_artifact()

    assert report.artifact_id == "artifact-1"
    assert report.weaknesses
    assert report.severity == Severity.MEDIUM
    assert report.attack_paths
    assert report.counterarguments
    assert report.failure_modes
    assert report.mitigations
    assert report.residual_risk == Severity.LOW
    assert report.pass_fail == PassFail.PASS
    assert report.rerun_recommendations
    assert artifact.evidence
    assert "stress_test" in artifact.tags


def test_stress_report_forces_fail_for_high_severity() -> None:
    report = StressTestReport(
        artifact_id="artifact-1",
        severity=Severity.HIGH,
        residual_risk=Severity.HIGH,
        pass_fail=PassFail.PASS,
        rerun_recommendations=["Rerun."],
    )

    assert report.pass_fail == PassFail.FAIL
