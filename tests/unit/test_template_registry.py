from __future__ import annotations

from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.template_registry import (
    get_research_project_template,
    list_research_project_templates,
)


def test_template_registry_lists_all_research_types() -> None:
    templates = list_research_project_templates()

    assert {template.template_id for template in templates} == set(ResearchProjectType)
    assert all(template.requires_human_review for template in templates)


def test_template_registry_sections_include_required_files() -> None:
    template = get_research_project_template(
        ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT
    )
    paths = {section.relative_path for section in template.sections}

    assert "README.md" in paths
    assert "docs/research_questions.md" in paths
    assert "docs/failure_taxonomy.md" in paths
    assert "lanes/00_master_ledger.md" in paths


def test_template_registry_safety_notes_are_explicit() -> None:
    template = get_research_project_template(ResearchProjectType.PAPER_SURVEY_PROJECT)

    assert any("no observed evidence" in note for note in template.safety_notes)
    assert any("Human review" in note for note in template.safety_notes)
