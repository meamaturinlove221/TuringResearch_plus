from __future__ import annotations

from turing_research_plus.project_template.research_types import (
    PROJECT_TYPE_DESCRIPTIONS,
    ResearchProjectType,
)
from turing_research_plus.project_template.template_registry import (
    get_research_project_template,
)


def test_research_type_descriptions_cover_all_types() -> None:
    assert set(PROJECT_TYPE_DESCRIPTIONS) == set(ResearchProjectType)


def test_each_research_type_has_distinct_recommendations() -> None:
    recommendations = {
        template_type: get_research_project_template(template_type).recommended_for
        for template_type in ResearchProjectType
    }

    assert "literature surveys" in recommendations[ResearchProjectType.PAPER_SURVEY_PROJECT]
    assert "research tools" in recommendations[ResearchProjectType.SOFTWARE_TOOLING_PROJECT]
    assert "geometry experiments" in recommendations[
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT
    ]
