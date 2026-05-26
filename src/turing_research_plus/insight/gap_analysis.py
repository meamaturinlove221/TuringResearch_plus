"""Gap validation for Deep Insight workflows."""

from __future__ import annotations

from turing_research_plus.insight.models import GapValidation, GapValidationReport
from turing_research_plus.survey.models import LiteratureSurveyArtifact


def analyze_gaps(
    survey_artifact: LiteratureSurveyArtifact,
    report_id: str = "gap-report-1",
) -> GapValidationReport:
    """Validate survey gaps with their attached evidence."""

    gaps: list[GapValidation] = []
    for gap in survey_artifact.gap_list.gaps:
        if not gap.evidence:
            raise ValueError("no gap without evidence")
        gaps.append(
            GapValidation(
                gap_id=gap.gap_id,
                description=gap.description,
                evidence=gap.evidence,
                validation_status="validated",
                confidence=0.75 if gap.severity == "medium" else 0.65,
            )
        )
    if not gaps:
        raise ValueError("gap validation requires at least one evidence-backed gap")
    return GapValidationReport(
        report_id=report_id,
        topic=survey_artifact.topic,
        gaps=gaps,
    )

