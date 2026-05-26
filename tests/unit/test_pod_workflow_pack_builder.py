from __future__ import annotations

from pathlib import Path

from turing_research_plus.pod_workflow.models import PodWorkflowPackBuildInput
from turing_research_plus.pod_workflow.pack_builder import build_vggt_modal_pod_workflow_pack

ROUTE_PACK = Path("examples") / "vggt-human-prior-survey" / "modal_sparseconv_route_pack"


def test_pod_workflow_pack_builder_writes_context_and_template(tmp_path: Path) -> None:
    pack = build_vggt_modal_pod_workflow_pack(
        PodWorkflowPackBuildInput(route_pack_dir=ROUTE_PACK, output_dir=tmp_path)
    )

    assert pack.route_id == "modal_sparseconv_real_v0"
    assert pack.requires_human_review is True
    assert "planned route only" in pack.warnings
    assert (tmp_path / "PROJECT_CONTEXT.md").exists()
    assert (tmp_path / "MEMORY.md").exists()
    assert (tmp_path / "ROUTE_SPEC.yaml").exists()
    assert (tmp_path / "STRUCTURED_OUTPUT_TEMPLATE" / "FINAL_STATUS.json").exists()
    assert "not executed by TuringResearch" in (tmp_path / "README.md").read_text(
        encoding="utf-8"
    )
