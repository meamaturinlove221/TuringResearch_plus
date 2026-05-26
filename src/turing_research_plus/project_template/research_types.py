"""Research project template types."""

from __future__ import annotations

from enum import StrEnum


class ResearchProjectType(StrEnum):
    """Supported reusable research project template types."""

    VGGT_LIKE_EXPERIMENT_PROJECT = "vggt_like_experiment_project"
    PAPER_SURVEY_PROJECT = "paper_survey_project"
    EXPERIMENT_HEAVY_PROJECT = "experiment_heavy_project"
    SOFTWARE_TOOLING_PROJECT = "software_tooling_project"
    MIXED_RESEARCH_PROJECT = "mixed_research_project"


PROJECT_TYPE_DESCRIPTIONS: dict[ResearchProjectType, str] = {
    ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT: (
        "Experiment-oriented template inspired by the VGGT review workflow, without "
        "VGGT-specific result claims."
    ),
    ResearchProjectType.PAPER_SURVEY_PROJECT: (
        "Literature-first template for digest, method cards, citation graph, and "
        "related-work positioning."
    ),
    ResearchProjectType.EXPERIMENT_HEAVY_PROJECT: (
        "Route, artifact, hard-gate, failure-taxonomy, and run-ingest heavy template."
    ),
    ResearchProjectType.SOFTWARE_TOOLING_PROJECT: (
        "Tooling and package-oriented template for research infrastructure projects."
    ),
    ResearchProjectType.MIXED_RESEARCH_PROJECT: (
        "Balanced template for projects that combine paper reading, experiments, and tools."
    ),
}
