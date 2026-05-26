from __future__ import annotations

from pathlib import Path

from turing_research_plus.project_template.generator import generate_research_project_template
from turing_research_plus.project_template.research_types import ResearchProjectType
from turing_research_plus.project_template.schema import ResearchProjectTemplateRequest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "project_templates" / "vggt_like_project"


def test_vggt_like_research_template_fixture_is_placeholder() -> None:
    required = [
        "README.md",
        "docs/north_star.md",
        "docs/research_questions.md",
        "docs/evidence_ledger.md",
        "docs/artifact_plan.md",
        "docs/experiment_routes.md",
        "docs/related_work.md",
        "docs/failure_taxonomy.md",
        "docs/advisor_pack.md",
        "lanes/00_master_ledger.md",
        "contracts/README.md",
        "examples/README.md",
        "race/feature_capsules/README.md",
    ]

    for relative_path in required:
        assert (FIXTURE / relative_path).exists()

    readme = (FIXTURE / "README.md").read_text(encoding="utf-8")
    evidence = (FIXTURE / "docs" / "evidence_ledger.md").read_text(encoding="utf-8")

    assert "template / placeholder" in readme
    assert "no observed evidence" in readme
    assert "`planned`" in evidence
    assert "SparseConv3D success" not in evidence


def test_generate_vggt_like_research_template_runtime(tmp_path: Path) -> None:
    result = generate_research_project_template(
        ResearchProjectTemplateRequest(
            project_id="vggt_runtime",
            project_name="VGGT Runtime Template",
            topic="Runtime generation",
            output_dir=tmp_path,
            template_type=ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT,
        )
    )

    assert len(result.generated_files) == 13
    assert result.template_type == ResearchProjectType.VGGT_LIKE_EXPERIMENT_PROJECT
    assert result.observed_evidence_generated is False
    assert (tmp_path / "docs" / "failure_taxonomy.md").exists()
