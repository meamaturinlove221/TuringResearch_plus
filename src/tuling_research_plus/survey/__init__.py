"""Literature survey workflow for TulingResearch Plus."""

from tuling_research_plus.survey.depth_gate import evaluate_depth_gates, full_text_ratio
from tuling_research_plus.survey.evidence_matrix import build_evidence_matrix
from tuling_research_plus.survey.gap_extractor import extract_gaps
from tuling_research_plus.survey.models import (
    EvidenceMatrix,
    GapList,
    LiteratureSurveyArtifact,
    MethodTaxonomy,
    PaperRecord,
    PaperScreeningTable,
    SurveyInput,
    SurveyPlan,
    SurveyResult,
    SurveyStatus,
    SurveyStrategy,
)
from tuling_research_plus.survey.service import LiteratureSurveyService
from tuling_research_plus.survey.strategies import create_survey_plan, strategy_defaults

__all__ = [
    "EvidenceMatrix",
    "GapList",
    "LiteratureSurveyArtifact",
    "LiteratureSurveyService",
    "MethodTaxonomy",
    "PaperRecord",
    "PaperScreeningTable",
    "SurveyInput",
    "SurveyPlan",
    "SurveyResult",
    "SurveyStatus",
    "SurveyStrategy",
    "build_evidence_matrix",
    "create_survey_plan",
    "evaluate_depth_gates",
    "extract_gaps",
    "full_text_ratio",
    "strategy_defaults",
]
