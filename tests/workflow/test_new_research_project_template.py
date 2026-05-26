from __future__ import annotations

from pathlib import Path

from turing_research_plus.project_template.generator import generate_project_template
from turing_research_plus.project_template.models import ProjectTemplateRequest

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "project_templates" / "vggt_like_project"


def test_vggt_like_project_template_fixture_contains_required_structure() -> None:
    required = [
        "README.md",
        "docs/north_star.md",
        "docs/evidence_ledger.md",
        "docs/artifact_plan.md",
        "docs/experiment_routes.md",
        "docs/related_work.md",
        "docs/advisor_pack.md",
        "lanes/00_master_ledger.md",
        "examples/README.md",
        "contracts/README.md",
        "race/feature_capsules/README.md",
    ]

    for relative_path in required:
        assert (FIXTURE / relative_path).exists()

    readme = (FIXTURE / "README.md").read_text(encoding="utf-8")
    ledger = (FIXTURE / "lanes" / "00_master_ledger.md").read_text(encoding="utf-8")
    evidence = (FIXTURE / "docs" / "evidence_ledger.md").read_text(encoding="utf-8")

    assert "It contains no experiment results" in readme
    assert "No experiment has been executed" in ledger
    assert "`planned`" in evidence
    assert "`observed`" not in evidence.splitlines()[5]


def test_new_research_project_template_runtime(tmp_path: Path) -> None:
    result = generate_project_template(
        ProjectTemplateRequest(
            project_id="new_project",
            project_name="New Research Project",
            topic="New research direction",
            output_dir=tmp_path,
        )
    )

    assert len(result.generated_files) == 11
    assert (tmp_path / "race" / "feature_capsules" / "README.md").exists()
    assert result.safety_warnings
    assert all("D:/vggt" not in item for item in result.safety_warnings)
