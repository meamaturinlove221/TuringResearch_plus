"""Build safe paper writing scaffolds."""

from __future__ import annotations

from pathlib import Path

from turing_research_plus.paper_write.evidence_linker import (
    build_vggt_evidence_requirements,
)
from turing_research_plus.paper_write.models import (
    PaperScaffold,
    PaperSectionPlan,
    PaperSectionStatus,
)


def build_vggt_paper_scaffold(
    knowledge_pack_dir: Path,
    *,
    scaffold_id: str = "vggt_human_prior_paper_scaffold",
) -> PaperScaffold:
    """Build a conservative VGGT paper scaffold from the research knowledge pack."""

    evidence_requirements = build_vggt_evidence_requirements(knowledge_pack_dir)
    missing_experiments = [
        "Run real SparseConv3D backend probe before any backend success claim.",
        "Generate board-level visual evidence inventory before results drafting.",
        "Collect artifact sha256 manifest for selected run outputs.",
    ]
    unsafe_claims = [
        "Do not claim SparseConv3D success.",
        "Do not claim full human completion.",
        "Do not claim final novelty against HART / HGGT / Fus3D without review.",
        "Do not report quantitative experiment numbers without real evidence.",
    ]

    return PaperScaffold(
        scaffold_id=scaffold_id,
        topic="VGGT / SMPL-X Human Prior",
        title_candidates=[
            "SMPL-X Feature Encoding for VGGT Human Geometry Completion",
            "Human-Prior Feature Injection for Feed-forward 3D Geometry",
        ],
        abstract_status=PaperSectionStatus.NEEDS_EVIDENCE,
        introduction_plan=PaperSectionPlan(
            section_id="introduction",
            title="Introduction",
            status=PaperSectionStatus.NEEDS_HUMAN_REVIEW,
            bullets=[
                "Frame the north star as SMPL-X feature encoding for VGGT.",
                "State the current work as research planning and evidence-gated development.",
            ],
            evidence_refs=[(knowledge_pack_dir / "north_star.md").as_posix()],
            human_review_notes=["Avoid final contribution claims until experiments exist."],
        ),
        related_work_plan=PaperSectionPlan(
            section_id="related_work",
            title="Related Work",
            status=PaperSectionStatus.NEEDS_EVIDENCE,
            bullets=[
                "Organize NeuralBody and HumanRAM as inspiration, not copied method claims.",
                "Keep HART, HGGT, Fus3D, and VGGT-HPE in requires-real-paper-review.",
            ],
            evidence_refs=[(knowledge_pack_dir / "related_work_positioning.md").as_posix()],
            missing_evidence=["Human paper review for closest related work."],
        ),
        method_plan=PaperSectionPlan(
            section_id="method",
            title="Method",
            status=PaperSectionStatus.OUTLINE_ONLY,
            bullets=[
                "Describe planned SMPL-X feature encoding route.",
                "Separate route design from validated implementation.",
            ],
            evidence_refs=[(knowledge_pack_dir / "method_taxonomy.md").as_posix()],
            missing_evidence=["Concrete architecture evidence from a successful run."],
        ),
        experiment_plan=PaperSectionPlan(
            section_id="experiments",
            title="Experiments",
            status=PaperSectionStatus.NEEDS_EVIDENCE,
            bullets=[
                "List Modal SparseConv3D route as planned experiment only.",
                "Define hard gates, artifacts, and fallback rules before execution.",
            ],
            evidence_refs=[(knowledge_pack_dir / "experiment_routes.md").as_posix()],
            missing_evidence=missing_experiments,
        ),
        results_status=PaperSectionStatus.NEEDS_EVIDENCE,
        limitation_plan=PaperSectionPlan(
            section_id="limitations",
            title="Limitations",
            status=PaperSectionStatus.NEEDS_HUMAN_REVIEW,
            bullets=[
                "State that current evidence is not enough for final experiment claims.",
                "State that visual readiness and artifact completeness remain blockers.",
            ],
            evidence_refs=[(knowledge_pack_dir / "visual_readiness.md").as_posix()],
            unsafe_claims=unsafe_claims,
        ),
        evidence_requirements=evidence_requirements,
        missing_experiments=missing_experiments,
        unsafe_claims=unsafe_claims,
        requires_human_review=True,
    )
