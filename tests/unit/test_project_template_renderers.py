from __future__ import annotations

from pathlib import Path

from turing_research_plus.project_template.renderers import render_research_template_file
from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import ResearchProjectTemplateRequest


def _request(template_type: ResearchProjectType) -> ResearchProjectTemplateRequest:
    return ResearchProjectTemplateRequest(
        project_id="demo",
        project_name="Demo",
        topic="Template rendering",
        output_dir=Path("out"),
        template_type=template_type,
    )


def test_render_readme_marks_template_placeholder() -> None:
    text = render_research_template_file(
        "README.md",
        _request(ResearchProjectType.MIXED_RESEARCH_PROJECT),
    )

    assert "template / placeholder" in text
    assert "no observed evidence" in text
    assert "no real citations" in text


def test_render_research_questions_varies_by_type() -> None:
    survey = render_research_template_file(
        "docs/research_questions.md",
        _request(ResearchProjectType.PAPER_SURVEY_PROJECT),
    )
    tooling = render_research_template_file(
        "docs/research_questions.md",
        _request(ResearchProjectType.SOFTWARE_TOOLING_PROJECT),
    )

    assert "Which papers define the method landscape?" in survey
    assert "Which public interface is being stabilized?" in tooling


def test_render_evidence_ledger_keeps_planned_status() -> None:
    text = render_research_template_file(
        "docs/evidence_ledger.md",
        _request(ResearchProjectType.EXPERIMENT_HEAVY_PROJECT),
    )

    assert "`planned`" in text
    assert "Do not mark template content as observed" in text
