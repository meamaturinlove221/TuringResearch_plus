from __future__ import annotations

from pathlib import Path

from turing_research_plus.project_template.generator import (
    generate_project_template,
    summarize_project_template,
)
from turing_research_plus.project_template.models import ProjectTemplateRequest


def _request(output_dir: Path, overwrite: bool = False) -> ProjectTemplateRequest:
    return ProjectTemplateRequest(
        project_id="demo_project",
        project_name="Demo Research Project",
        topic="Demo topic",
        output_dir=output_dir,
        north_star="Test a research idea without claiming results.",
        overwrite=overwrite,
    )


def test_project_template_generator_creates_required_files(tmp_path: Path) -> None:
    result = generate_project_template(_request(tmp_path))
    required = {
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
    }

    assert {item.relative_path for item in result.generated_files} == required
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "docs" / "north_star.md").exists()
    assert result.requires_human_review is True
    assert result.network_used is False
    assert result.read_private_vggt is False


def test_project_template_generator_does_not_overwrite_by_default(
    tmp_path: Path,
) -> None:
    readme = tmp_path / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text("existing", encoding="utf-8")

    result = generate_project_template(_request(tmp_path))

    assert readme.read_text(encoding="utf-8") == "existing"
    assert "README.md: already exists" in result.omitted_items


def test_project_template_generator_can_overwrite_when_requested(
    tmp_path: Path,
) -> None:
    readme = tmp_path / "README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text("existing", encoding="utf-8")

    result = generate_project_template(_request(tmp_path, overwrite=True))
    summary = summarize_project_template(result)

    assert "Demo Research Project" in readme.read_text(encoding="utf-8")
    assert "Generated Files" in summary
    assert any(item.overwrite for item in result.generated_files)
