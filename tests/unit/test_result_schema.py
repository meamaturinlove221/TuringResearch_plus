from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.experiment.design import design_experiment
from tuling_research_plus.experiment.result_schema import analyze_result, generate_result_schema
from tuling_research_plus.experiment.service import ExperimentExecutionService
from tuling_research_plus.experiment.tools import (
    research_result_analyze,
    research_result_schema_generate,
)
from tuling_research_plus.hypothesis.falsifiability import build_hypothesis
from tuling_research_plus.hypothesis.models import GapPriority, Hypothesis


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="paper-1",
        locator="section-3",
        quote="Evidence gates reduce unsupported claims.",
    )


def hypothesis() -> Hypothesis:
    return build_hypothesis(
        GapPriority(
            gap_id="gap-1",
            description="Few studies validate workflow gates.",
            score=0.9,
            rationale="High confidence and enough evidence.",
            evidence=[evidence()],
        )
    )


def test_result_schema_generated_from_metrics() -> None:
    plan = design_experiment(hypothesis())
    schema = generate_result_schema(plan)

    metric_fields = [field for field in schema.fields if field.name.startswith("metric_")]
    assert schema.schema_id == "result-schema-experiment-plan-1"
    assert len(metric_fields) == len(plan.metrics)


def test_result_analyze_parses_dry_run_metrics() -> None:
    plan = design_experiment(hypothesis())
    schema = generate_result_schema(plan)
    analysis = analyze_result(plan, schema, raw_result={"metric_1": 0.3})

    assert analysis.metrics_observed["metric_1"] == 0.3
    assert analysis.evidence_refs


def test_result_schema_and_analyze_tools_return_json_payloads() -> None:
    service = ExperimentExecutionService()
    plan = design_experiment(hypothesis())
    schema = generate_result_schema(plan)
    schema_payload = research_result_schema_generate(plan, service)
    analysis_payload = research_result_analyze(
        plan,
        schema,
        service,
        raw_result={"metric_1": 0.3},
    )

    assert schema_payload["fields"]
    assert analysis_payload["metrics_observed"]["metric_1"] == 0.3

