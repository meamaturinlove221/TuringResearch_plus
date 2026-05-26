"""Experiment result schema and analysis."""

from __future__ import annotations

from typing import Any

from turing_research_plus.experiment.models import (
    ExperimentPlan,
    ExperimentResultAnalysis,
    ResultSchema,
    ResultSchemaField,
)


def generate_result_schema(plan: ExperimentPlan) -> ResultSchema:
    """Generate a result schema for a plan."""

    fields = [
        ResultSchemaField(
            name="plan_id",
            field_type="string",
            description="Experiment plan id.",
        ),
        ResultSchemaField(
            name="status",
            field_type="string",
            description="Dry-run result status.",
        ),
    ]
    fields.extend(
        ResultSchemaField(
            name=f"metric_{index}",
            field_type="number",
            description=f"Observed metric: {metric}.",
        )
        for index, metric in enumerate(plan.metrics, start=1)
    )
    return ResultSchema(
        schema_id=f"result-schema-{plan.plan_id}",
        plan_id=plan.plan_id,
        fields=fields,
    )


def analyze_result(
    plan: ExperimentPlan,
    schema: ResultSchema,
    raw_result: dict[str, Any] | None = None,
) -> ExperimentResultAnalysis:
    """Analyze a dry-run result with deterministic defaults."""

    raw = raw_result or {}
    metrics = {
        field.name: float(raw.get(field.name, 0.0))
        for field in schema.fields
        if field.field_type == "number"
    }
    conclusion = (
        "Result schema is ready; real execution has not been run."
        if not metrics
        else "Dry-run result parsed against generated schema."
    )
    return ExperimentResultAnalysis(
        plan_id=plan.plan_id,
        result_schema_id=schema.schema_id,
        metrics_observed=metrics,
        conclusion=conclusion,
        evidence_refs=plan.evidence_refs,
        raw_result=raw,
    )
