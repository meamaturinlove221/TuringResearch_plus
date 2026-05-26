from __future__ import annotations

from pathlib import Path

from turing_research_plus.project_template.generator import generate_research_project_template
from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import ResearchProjectTemplateRequest

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "examples" / "project_templates"


def test_generic_research_template_fixtures_are_placeholder_safe() -> None:
    for fixture_name in [
        "paper_survey_project",
        "experiment_heavy_project",
        "software_tooling_project",
    ]:
        root = BASE / fixture_name
        readme = (root / "README.md").read_text(encoding="utf-8")
        evidence = (root / "docs" / "evidence_ledger.md").read_text(encoding="utf-8")
        related_work = (root / "docs" / "related_work.md").read_text(encoding="utf-8")

        assert "template / placeholder" in readme
        assert "no observed evidence" in readme
        assert "`planned`" in evidence
        assert "No real citation" in related_work
        assert "D:/vggt" not in readme


def test_generate_mixed_research_project_runtime(tmp_path: Path) -> None:
    result = generate_research_project_template(
        ResearchProjectTemplateRequest(
            project_id="mixed_runtime",
            project_name="Mixed Runtime Template",
            topic="Runtime generation",
            output_dir=tmp_path,
            template_type=ResearchProjectType.MIXED_RESEARCH_PROJECT,
            research_questions=["What is missing?", "What evidence would change the plan?"],
        )
    )
    questions = (tmp_path / "docs" / "research_questions.md").read_text(encoding="utf-8")

    assert result.requires_human_review is True
    assert result.network_used is False
    assert result.read_private_vggt is False
    assert "What is missing?" in questions
    assert (tmp_path / "race" / "feature_capsules" / "README.md").exists()
