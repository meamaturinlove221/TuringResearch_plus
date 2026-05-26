"""Experiment Execution workflow service."""

from __future__ import annotations

from typing import Any

from turing_research_plus.experiment.constraints import analyze_constraints
from turing_research_plus.experiment.design import design_experiment
from turing_research_plus.experiment.implementation import build_implementation_plan
from turing_research_plus.experiment.models import (
    ConstraintAnalysis,
    ExperimentPlan,
    ExperimentResultAnalysis,
    ImplementationPlan,
    ResultSchema,
    ScenarioPlan,
)
from turing_research_plus.experiment.result_schema import analyze_result, generate_result_schema
from turing_research_plus.experiment.scenario import plan_scenarios
from turing_research_plus.hypothesis.models import Hypothesis


class ExperimentExecutionService:
    """Create experiment plans and result schemas from validated hypotheses."""

    def experiment_design(self, hypothesis: Hypothesis) -> ExperimentPlan:
        """Design an experiment."""

        return design_experiment(hypothesis)

    def constraint_analyze(self, plan: ExperimentPlan) -> ConstraintAnalysis:
        """Analyze plan constraints."""

        return analyze_constraints(plan)

    def scenario_plan(self, plan: ExperimentPlan) -> ScenarioPlan:
        """Create scenario plan."""

        return plan_scenarios(plan)

    def implementation_plan(self, plan: ExperimentPlan) -> ImplementationPlan:
        """Create implementation plan."""

        return build_implementation_plan(plan)

    def result_schema_generate(self, plan: ExperimentPlan) -> ResultSchema:
        """Generate result schema."""

        return generate_result_schema(plan)

    def result_analyze(
        self,
        plan: ExperimentPlan,
        schema: ResultSchema,
        raw_result: dict[str, Any] | None = None,
    ) -> ExperimentResultAnalysis:
        """Analyze a dry-run result."""

        return analyze_result(plan, schema, raw_result=raw_result)
