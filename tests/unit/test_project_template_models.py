from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.project_template.models import (
    ProjectTemplateFile,
    ProjectTemplateRequest,
    ProjectTemplateResult,
)


def test_project_template_request_serializes() -> None:
    request = ProjectTemplateRequest(
        project_id="demo_project",
        project_name="Demo Project",
        topic="Research workflow",
        output_dir=Path("out"),
    )

    payload = request.model_dump(mode="json")

    assert payload["project_id"] == "demo_project"
    assert payload["overwrite"] is False


def test_project_template_request_rejects_unsafe_project_id() -> None:
    with pytest.raises(ValueError, match="path-safe slug"):
        ProjectTemplateRequest(
            project_id="../demo",
            project_name="Demo Project",
            topic="Research workflow",
            output_dir=Path("out"),
        )


def test_project_template_result_rejects_private_vggt_read() -> None:
    with pytest.raises(ValueError, match="must not read private VGGT"):
        ProjectTemplateResult(
            project_id="demo",
            project_name="Demo",
            output_dir="out",
            generated_files=[
                ProjectTemplateFile(relative_path="README.md", role="readme")
            ],
            read_private_vggt=True,
        )


def test_project_template_result_rejects_network_use() -> None:
    with pytest.raises(ValueError, match="must not use network"):
        ProjectTemplateResult(
            project_id="demo",
            project_name="Demo",
            output_dir="out",
            network_used=True,
        )
