"""Thin research.experiment_* tool wrappers."""

from __future__ import annotations

from typing import Any

from turing_research_plus.experiment.models import ExperimentPlan, ResultSchema
from turing_research_plus.experiment.service import ExperimentExecutionService
from turing_research_plus.hypothesis.models import Hypothesis


def research_experiment_design(
    hypothesis: Hypothesis,
    service: ExperimentExecutionService,
) -> dict[str, Any]:
    return service.experiment_design(hypothesis).model_dump(mode="json")


def research_constraint_analyze(
    plan: ExperimentPlan,
    service: ExperimentExecutionService,
) -> dict[str, Any]:
    return service.constraint_analyze(plan).model_dump(mode="json")


def research_scenario_plan(
    plan: ExperimentPlan,
    service: ExperimentExecutionService,
) -> dict[str, Any]:
    return service.scenario_plan(plan).model_dump(mode="json")


def research_implementation_plan(
    plan: ExperimentPlan,
    service: ExperimentExecutionService,
) -> dict[str, Any]:
    return service.implementation_plan(plan).model_dump(mode="json")


def research_result_schema_generate(
    plan: ExperimentPlan,
    service: ExperimentExecutionService,
) -> dict[str, Any]:
    return service.result_schema_generate(plan).model_dump(mode="json")


def research_result_analyze(
    plan: ExperimentPlan,
    schema: ResultSchema,
    service: ExperimentExecutionService,
    raw_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return service.result_analyze(plan, schema, raw_result=raw_result).model_dump(mode="json")

