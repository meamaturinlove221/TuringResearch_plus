from __future__ import annotations

from pathlib import Path

PACK_ROOT = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "research_knowledge_pack"
)


REQUIRED_FILES = {
    "README.md",
    "north_star.md",
    "current_state.md",
    "evidence_summary.md",
    "artifact_summary.md",
    "visual_readiness.md",
    "failure_taxonomy.md",
    "experiment_routes.md",
    "related_work_positioning.md",
    "method_taxonomy.md",
    "vault_graph.md",
    "advisor_brief.md",
    "next_actions.md",
    "manifest.yaml",
}


def test_research_knowledge_pack_files_exist() -> None:
    missing = [name for name in sorted(REQUIRED_FILES) if not (PACK_ROOT / name).exists()]

    assert missing == []


def test_research_knowledge_pack_preserves_claim_boundaries() -> None:
    combined = "\n".join((PACK_ROOT / name).read_text(encoding="utf-8") for name in REQUIRED_FILES)

    assert "SMPL-X direct replacement -> SMPL-X feature encoding for VGGT" in combined
    assert "SparseConv3D success is not claimed" in combined
    assert "no_sparseconv3d_success_claim" in combined
    assert "requires-human-review" in combined
    assert "not-enough-evidence" in combined
    assert "No VGGT experiment was run" in combined or "no_vggt_experiment_run" in combined


def test_current_state_keeps_sparseconv3d_unproven() -> None:
    current_state = (PACK_ROOT / "current_state.md").read_text(encoding="utf-8")

    assert "| V260 | hard-blocked |" in current_state
    assert "| V999-SparseConv3D | not-enough-evidence |" in current_state
    assert (
        "| Later Modal SparseConv3D route | planned / requires-real-experiment |"
        in current_state
    )
    assert "SparseConv3D success" not in current_state.replace(
        "SparseConv3D backend success is not established by current local evidence.",
        "",
    )
