from tuling_research_plus.stress.counterfactual import counterfactual_probe, failure_mode_analyze
from tuling_research_plus.stress.models import FailureMode, PassFail, Severity
from tuling_research_plus.stress.service import StressTestService
from tuling_research_plus.stress.tools import (
    research_counterfactual_probe,
    research_failure_mode_analyze,
)


def test_counterfactual_probe_flags_no_evidence() -> None:
    report = counterfactual_probe(
        artifact_id="artifact-1",
        claim="Evidence gate works.",
        evidence_count=0,
    )

    assert report.pass_fail == PassFail.FAIL
    assert report.severity == Severity.HIGH


def test_mitigation_lowers_residual_risk() -> None:
    report = counterfactual_probe(
        artifact_id="artifact-1",
        claim="Evidence gate works.",
        evidence_count=0,
        mitigated=True,
    )

    assert report.severity == Severity.HIGH
    assert report.residual_risk == Severity.LOW
    assert report.pass_fail == PassFail.PASS


def test_failure_mode_analyze_tool_returns_json_payload() -> None:
    failure_modes = [
        FailureMode(
            mode_id="mode-1",
            description="Evidence source is non-representative.",
            severity=Severity.HIGH,
            mitigation="Add independent evidence.",
        )
    ]
    report = failure_mode_analyze(
        artifact_id="artifact-1",
        failure_modes=failure_modes,
        mitigations=["Add independent evidence."],
    )
    counterfactual_payload = research_counterfactual_probe(
        artifact_id="artifact-1",
        claim="Evidence gate works.",
        evidence_count=0,
        service=StressTestService(),
        mitigated=True,
    )
    failure_payload = research_failure_mode_analyze(
        artifact_id="artifact-1",
        failure_modes=failure_modes,
        service=StressTestService(),
        mitigations=["Add independent evidence."],
    )

    assert report.residual_risk == Severity.LOW
    assert counterfactual_payload["pass_fail"] == "pass"
    assert failure_payload["mitigations"]

