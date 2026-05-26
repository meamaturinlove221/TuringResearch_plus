"""Literature survey workflow for TuringResearch Plus."""

from turing_research_plus.survey.depth_gate import evaluate_depth_gates, full_text_ratio
from turing_research_plus.survey.evidence_matrix import build_evidence_matrix
from turing_research_plus.survey.gap_extractor import extract_gaps
from turing_research_plus.survey.models import (
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
from turing_research_plus.survey.service import LiteratureSurveyService
from turing_research_plus.survey.strategies import create_survey_plan, strategy_defaults

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
