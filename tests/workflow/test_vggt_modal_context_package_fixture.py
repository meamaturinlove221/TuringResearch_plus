from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.pod_workflow.models import PodWorkflowPackBuildInput
from turing_research_plus.pod_workflow.pack_builder import build_vggt_modal_pod_workflow_pack

FIXTURE = Path("examples") / "vggt-human-prior-survey" / "pod_workflow_pack"
ROUTE_PACK = Path("examples") / "vggt-human-prior-survey" / "modal_sparseconv_route_pack"


def test_vggt_modal_context_package_fixture_exists() -> None:
    assert (FIXTURE / "PROJECT_CONTEXT.md").exists()
    assert (FIXTURE / "MEMORY.md").exists()
    assert (FIXTURE / "ROUTE_SPEC.yaml").exists()
    assert (FIXTURE / "STRUCTURED_OUTPUT_TEMPLATE" / "FINAL_STATUS.json").exists()
    assert "planned" in (FIXTURE / "ROUTE_SPEC.yaml").read_text(encoding="utf-8")
    assert "not executed by TuringResearch" in (FIXTURE / "README.md").read_text(
        encoding="utf-8"
    )
    final_status = json.loads(
        (FIXTURE / "STRUCTURED_OUTPUT_TEMPLATE" / "FINAL_STATUS.json").read_text(
            encoding="utf-8"
        )
    )
    assert final_status["sparseconv3d_success_claimed"] is False


def test_vggt_modal_context_package_can_be_rebuilt(tmp_path: Path) -> None:
    pack = build_vggt_modal_pod_workflow_pack(
        PodWorkflowPackBuildInput(route_pack_dir=ROUTE_PACK, output_dir=tmp_path)
    )

    assert pack.context_package.requires_human_review is True
    assert "FINAL_STATUS.json" in pack.structured_output_template.output_files
    assert (tmp_path / "STRUCTURED_OUTPUT_TEMPLATE" / "PROPOSED_EVIDENCE_UPDATES.json").exists()
