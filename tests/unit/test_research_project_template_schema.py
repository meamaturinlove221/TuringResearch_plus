from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import (
    ResearchProjectTemplate,
    ResearchProjectTemplateManifest,
    ResearchProjectTemplateRequest,
    ResearchTemplateSection,
)


def test_research_project_template_request_serializes() -> None:
    request = ResearchProjectTemplateRequest(
        project_id="demo",
        project_name="Demo",
        topic="Template test",
        output_dir=Path("out"),
        template_type=ResearchProjectType.PAPER_SURVEY_PROJECT,
    )

    payload = request.model_dump(mode="json")

    assert payload["template_type"] == "paper_survey_project"
    assert payload["project_id"] == "demo"


def test_research_project_template_request_rejects_unsafe_id() -> None:
    with pytest.raises(ValueError, match="path-safe slug"):
        ResearchProjectTemplateRequest(
            project_id="../demo",
            project_name="Demo",
            topic="Template test",
            output_dir=Path("out"),
        )


def test_research_project_template_requires_readme() -> None:
    with pytest.raises(ValueError, match="README.md"):
        ResearchProjectTemplate(
            template_id=ResearchProjectType.MIXED_RESEARCH_PROJECT,
            display_name="Mixed",
            description="Mixed template",
            sections=[
                ResearchTemplateSection(
                    relative_path="docs/north_star.md",
                    title="North Star",
                    role="north-star",
                )
            ],
        )


def test_research_project_template_manifest_rejects_observed_evidence() -> None:
    with pytest.raises(ValueError, match="must not generate observed evidence"):
        ResearchProjectTemplateManifest(
            project_id="demo",
            project_name="Demo",
            template_type=ResearchProjectType.MIXED_RESEARCH_PROJECT,
            output_dir="out",
            observed_evidence_generated=True,
        )


def test_research_project_template_manifest_rejects_network() -> None:
    with pytest.raises(ValueError, match="must not use network"):
        ResearchProjectTemplateManifest(
            project_id="demo",
            project_name="Demo",
            template_type=ResearchProjectType.MIXED_RESEARCH_PROJECT,
            output_dir="out",
            network_used=True,
        )
