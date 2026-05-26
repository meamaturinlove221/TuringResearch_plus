"""Hypothesis Formation workflow service."""

from __future__ import annotations

from turing_research_plus.hypothesis.falsifiability import build_hypothesis, is_falsifiable
from turing_research_plus.hypothesis.finer import formulate_research_question
from turing_research_plus.hypothesis.models import (
    GapPriorityReport,
    Hypothesis,
    HypothesisPortfolio,
    HypothesisSet,
    OperationalizedHypothesis,
    ResearchQuestion,
)
from turing_research_plus.hypothesis.portfolio import build_portfolio
from turing_research_plus.hypothesis.scoring import prioritize_gaps, score_hypothesis
from turing_research_plus.insight.models import GapValidationReport, InsightReport


class HypothesisFormationService:
    """Build ranked falsifiable hypotheses from validated gaps and insights."""

    def gap_prioritize(self, gap_report: GapValidationReport) -> GapPriorityReport:
        """Prioritize validated gaps."""

        return prioritize_gaps(gap_report)

    def hypothesis_generate(
        self,
        gap_priorities: GapPriorityReport,
        insight_report: InsightReport | None = None,
    ) -> HypothesisSet:
        """Generate scored falsifiable hypotheses."""

        hypotheses: list[Hypothesis] = []
        for index, priority in enumerate(gap_priorities.priorities, start=1):
            hypothesis = build_hypothesis(priority, index=index)
            if insight_report is not None and insight_report.insights:
                hypothesis = hypothesis.model_copy(
                    update={
                        "mechanism": (
                            f"{hypothesis.mechanism} Insight anchor: "
                            f"{insight_report.insights[0].statement}"
                        )
                    }
                )
            scored = score_hypothesis(hypothesis, priority)
            if not is_falsifiable(scored):
                raise ValueError("generated hypothesis is not falsifiable")
            hypotheses.append(scored)
        return HypothesisSet(
            set_id="hypothesis-set-1",
            topic=gap_priorities.topic,
            hypotheses=hypotheses,
        )

    def hypothesis_operationalize(self, hypothesis: Hypothesis) -> OperationalizedHypothesis:
        """Create a concrete variable and measurement plan."""

        return OperationalizedHypothesis(
            hypothesis_id=hypothesis.hypothesis_id,
            variables={
                "independent": hypothesis.independent_variables,
                "dependent": hypothesis.dependent_variables,
                "control": hypothesis.control_variables,
            },
            measurement_plan=(
                f"Measure {', '.join(hypothesis.dependent_variables)} after varying "
                f"{', '.join(hypothesis.independent_variables)}."
            ),
            experiment_readiness="dry_run_ready",
            evidence_refs=hypothesis.evidence_refs,
        )

    def research_question_formulate(self, hypothesis: Hypothesis) -> ResearchQuestion:
        """Formulate a precise research question."""

        return formulate_research_question(hypothesis)

    def hypothesis_portfolio_build(
        self,
        hypothesis_set: HypothesisSet,
        max_items: int = 3,
    ) -> HypothesisPortfolio:
        """Build a compact hypothesis portfolio."""

        return build_portfolio(hypothesis_set, max_items=max_items)
