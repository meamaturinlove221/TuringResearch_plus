from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.stress.models import ExperimentPlan, PassFail, Severity
from turing_research_plus.stress.premortem import experiment_premortem
from turing_research_plus.stress.service import StressTestService
from turing_research_plus.stress.tools import research_experiment_premortem


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def weak_plan() -> ExperimentPlan:
    return ExperimentPlan(
        plan_id="plan-1",
        title="Weak experiment plan",
        hypothesis_link="hypothesis-1",
        design="dry-run comparison",
    )


def strong_plan() -> ExperimentPlan:
    return ExperimentPlan(
        plan_id="plan-1",
        title="Strong experiment plan",
        hypothesis_link="hypothesis-1",
        design="dry-run comparison",
        required_data=["baseline output", "gated output"],
        metrics=["unsupported claim rate"],
        controls=["topic scope"],
        success_criteria=["unsupported claim rate decreases"],
        evidence_refs=[evidence()],
    )


def test_weak_experiment_plan_is_rejected() -> None:
    report = experiment_premortem(weak_plan())

    assert report.pass_fail == PassFail.FAIL
    assert report.severity == Severity.HIGH
    assert {weakness.weakness_id for weakness in report.weaknesses} >= {
        "experiment-missing-data",
        "experiment-missing-metrics",
        "experiment-missing-success-criteria",
    }


def test_strong_experiment_plan_passes_with_low_residual_risk() -> None:
    report = experiment_premortem(strong_plan())

    assert report.pass_fail == PassFail.PASS
    assert report.residual_risk == Severity.LOW


def test_experiment_premortem_tool_returns_json_payload() -> None:
    payload = research_experiment_premortem(weak_plan(), StressTestService())

    assert payload["pass_fail"] == "fail"
    assert payload["failure_modes"]
