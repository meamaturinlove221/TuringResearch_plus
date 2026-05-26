"""Deep Insight workflow service."""

from __future__ import annotations

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.insight.boundary import build_boundary_map
from turing_research_plus.insight.gap_analysis import analyze_gaps
from turing_research_plus.insight.models import (
    BoundaryMap,
    DeepInsightResult,
    GapValidationReport,
    InsightItem,
    InsightReport,
    ReformulatedProblemSet,
    SensitivityReport,
)
from turing_research_plus.insight.reformulation import reformulate_problems
from turing_research_plus.insight.sensitivity import probe_sensitivity
from turing_research_plus.survey.models import LiteratureSurveyArtifact


class DeepInsightService:
    """Convert survey artifacts into insight reports and problem reformulations."""

    def gap_analyze(self, survey_artifact: LiteratureSurveyArtifact) -> GapValidationReport:
        """Validate evidence-backed gaps."""

        return analyze_gaps(survey_artifact)

    def insight_generate(self, gap_report: GapValidationReport) -> InsightReport:
        """Synthesize insights with supporting and contradicting evidence."""

        insights: list[InsightItem] = []
        for index, gap in enumerate(gap_report.gaps, start=1):
            supporting = gap.evidence
            contradicting = [self._contradicting_evidence(gap.evidence[0], index)]
            insights.append(
                InsightItem(
                    insight_id=f"insight-{index}",
                    statement=(
                        "The most useful next step is to test the boundary of "
                        f"{gap.description}"
                    ),
                    supporting_evidence=supporting,
                    contradicting_evidence=contradicting,
                    implication="Prioritize boundary checks before broad implementation.",
                )
            )
        return InsightReport(
            report_id="insight-report-1",
            topic=gap_report.topic,
            insights=insights,
        )

    def boundary_map(self, gap_report: GapValidationReport) -> BoundaryMap:
        """Build a boundary map."""

        return build_boundary_map(gap_report)

    def sensitivity_probe(self, gap_report: GapValidationReport) -> SensitivityReport:
        """Build a sensitivity report."""

        return probe_sensitivity(gap_report)

    def problem_reformulate(self, gap_report: GapValidationReport) -> ReformulatedProblemSet:
        """Build reformulated problems."""

        return reformulate_problems(gap_report)

    def run(self, survey_artifact: LiteratureSurveyArtifact) -> DeepInsightResult:
        """Run the full deterministic Deep Insight workflow."""

        gap_report = self.gap_analyze(survey_artifact)
        return DeepInsightResult(
            gap_validation_report=gap_report,
            insight_report=self.insight_generate(gap_report),
            boundary_map=build_boundary_map(gap_report),
            sensitivity_report=probe_sensitivity(gap_report),
            reformulated_problem_set=reformulate_problems(gap_report),
        )

    def _contradicting_evidence(self, source: EvidenceRef, index: int) -> EvidenceRef:
        return EvidenceRef(
            source_id=f"{source.source_id}:counterpoint",
            locator=f"{source.locator}:limitation",
            quote=(
                "Counter-evidence placeholder: the same source indicates limits, "
                f"scope uncertainty, or missing comparison for insight {index}."
            ),
            url=source.url,
            confidence=source.confidence,
        )
