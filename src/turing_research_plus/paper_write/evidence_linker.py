"""Evidence linking helpers for paper writing scaffolds."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.models import EvidenceRequirement


def build_vggt_evidence_requirements(knowledge_pack_dir: Path) -> list[EvidenceRequirement]:
    """Build conservative VGGT evidence requirements from known pack files."""

    refs = [
        (knowledge_pack_dir / "evidence_summary.md").as_posix(),
        (knowledge_pack_dir / "experiment_routes.md").as_posix(),
        (knowledge_pack_dir / "visual_readiness.md").as_posix(),
    ]
    return [
        EvidenceRequirement(
            requirement_id="exp-real-sparse-backend",
            section="experiments",
            description="Real SparseConv3D backend probe and run artifact manifest.",
            status="missing",
            source_refs=refs,
        ),
        EvidenceRequirement(
            requirement_id="visual-board-inventory",
            section="results",
            description=(
                "Board-level visual evidence for full-body, hairline, and "
                "hand/object cases."
            ),
            status="missing",
            source_refs=refs,
        ),
        EvidenceRequirement(
            requirement_id="related-work-paper-review",
            section="related_work",
            description="Human review for HART, HGGT, Fus3D, VGGT-HPE, NeuralBody, and HumanRAM.",
            status="requires-human-review",
            source_refs=[(knowledge_pack_dir / "related_work_positioning.md").as_posix()],
        ),
    ]


def missing_evidence_report(requirements: list[EvidenceRequirement]) -> list[str]:
    """Return human-readable missing evidence lines."""

    return [
        f"- `{item.requirement_id}` ({item.section}): {item.description} [{item.status}]"
        for item in requirements
        if item.status in {"missing", "requires-human-review", "not-enough-evidence"}
    ]
