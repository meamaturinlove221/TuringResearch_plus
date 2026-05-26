"""Three-pass reading plan templates."""

from __future__ import annotations

from turing_research_plus.scholar_pipeline.models import ThreePassReadingPlan


def build_three_pass_reading_plan(paper_id: str, title: str) -> ThreePassReadingPlan:
    """Build a Keshav-style three-pass reading plan for a paper."""

    return ThreePassReadingPlan(
        paper_id=paper_id,
        title=title,
        pass_1=[
            "Read title, abstract, introduction, section headings, figures, and conclusion.",
            "Record task, claimed contribution, and whether the paper is relevant to VGGT.",
            "Do not mark the paper as fully reviewed in this pass.",
        ],
        pass_2=[
            "Read the method and experiment sections closely enough to extract inputs, "
            "outputs, and representation.",
            "Draft a PaperMethodCard with evidence refs and limitations.",
            "Record borrow / not-copy notes and collision-risk questions.",
        ],
        pass_3=[
            "Reconstruct the method mechanics, assumptions, and failure modes.",
            "Map SMPL / SMPL-X, voxel, tri-plane, token, and geometry relevance to VGGT.",
            "Update collision notes only after checking the cited evidence.",
        ],
        requires_real_paper_review=True,
        human_verified=False,
    )
