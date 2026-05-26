from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.git_handoff.structured_output import (
    build_structured_output_template,
    write_structured_output_template,
)


def test_structured_output_template_lists_required_files() -> None:
    template = build_structured_output_template(route_id="route")

    assert "RUN_STATUS.json" in template.output_files
    assert "FINAL_STATUS.json" in template.output_files
    assert "PROPOSED_EVIDENCE_UPDATES.json" in template.output_files
    assert template.requires_human_review is True


def test_write_structured_output_template(tmp_path: Path) -> None:
    template = build_structured_output_template(route_id="route")
    write_structured_output_template(tmp_path, template)

    assert (tmp_path / "RUN_STATUS.json").exists()
    assert (tmp_path / "FINAL_STATUS.json").exists()
    assert (tmp_path / "ARTIFACT_INDEX.md").exists()
    final_status = json.loads((tmp_path / "FINAL_STATUS.json").read_text(encoding="utf-8"))
    assert final_status["sparseconv3d_success_claimed"] is False
    assert final_status["execution_status"] == "not_executed_by_turingresearch"
