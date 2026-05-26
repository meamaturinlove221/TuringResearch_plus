"""Build conservative related-work draft skeletons."""

from __future__ import annotations

from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.paper_write.citation_safety import (
    CitationSafetyReport,
    RelatedWorkCitation,
    citation_from_digest_fixture,
    evaluate_citation_safety,
    render_citation_safety_report,
)


class RelatedWorkDraftSkeleton(BaseModel):
    """Review-only related-work skeleton."""

    model_config = ConfigDict(extra="forbid")

    skeleton_id: str = Field(min_length=1)
    project_topic: str = Field(min_length=1)
    feed_forward_geometry: list[str] = Field(default_factory=list)
    human_prior_smplx: list[str] = Field(default_factory=list)
    neural_body_sparse_voxel: list[str] = Field(default_factory=list)
    triplane_rasterized_pose_feature: list[str] = Field(default_factory=list)
    vggt_human_extensions: list[str] = Field(default_factory=list)
    difference_from_our_route: list[str] = Field(default_factory=list)
    requires_review_list: list[str] = Field(default_factory=list)
    unsafe_claims_list: list[str] = Field(default_factory=list)
    citations: list[RelatedWorkCitation] = Field(default_factory=list)
    citation_safety: CitationSafetyReport
    evidence_refs: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    generated_camera_ready_text: bool = False
    fabricated_citations: bool = False

    @model_validator(mode="after")
    def related_work_skeleton_stays_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("related-work skeleton requires human review")
        if self.generated_camera_ready_text:
            raise ValueError("related-work skeleton must not generate camera-ready text")
        if self.fabricated_citations:
            raise ValueError("related-work skeleton must not fabricate citations")
        if not self.citations:
            raise ValueError("related-work skeleton must include citation candidates")
        if any(not citation.source_status for citation in self.citations):
            raise ValueError("every citation candidate requires source_status")
        if not self.requires_review_list:
            raise ValueError("related-work skeleton must list review requirements")
        if not self.unsafe_claims_list:
            raise ValueError("related-work skeleton must list unsafe claims")
        return self


def build_vggt_related_work_draft_skeleton(
    related_work_dir: Path,
    collision_risk_dir: Path,
    paper_digest_dir: Path,
    *,
    skeleton_id: str = "vggt_related_work_draft_skeleton",
) -> RelatedWorkDraftSkeleton:
    """Build a conservative VGGT related-work skeleton from local reports."""

    digest_citations = [
        citation_from_digest_fixture(path)
        for path in sorted(paper_digest_dir.glob("*_digest.fixture.md"))
    ]
    review_citations = [
        RelatedWorkCitation(
            citation_id="hart-review-needed",
            title="HART",
            source_status="requires-real-paper-review",
            evidence_refs=[(related_work_dir / "requires_review.md").as_posix()],
        ),
        RelatedWorkCitation(
            citation_id="vggt-hpe-review-needed",
            title="VGGT-HPE",
            source_status="requires-real-paper-review",
            evidence_refs=[(related_work_dir / "requires_review.md").as_posix()],
        ),
        RelatedWorkCitation(
            citation_id="hggt-review-needed",
            title="HGGT",
            source_status="requires-real-paper-review",
            evidence_refs=[(related_work_dir / "requires_review.md").as_posix()],
        ),
        RelatedWorkCitation(
            citation_id="fus3d-review-needed",
            title="Fus3D",
            source_status="requires-real-paper-review",
            evidence_refs=[(related_work_dir / "requires_review.md").as_posix()],
        ),
    ]
    citations = [*digest_citations, *review_citations]
    citation_safety = evaluate_citation_safety(citations)
    evidence_refs = [
        (related_work_dir / "related_work_positioning.md").as_posix(),
        (related_work_dir / "safe_related_work_claims.md").as_posix(),
        (related_work_dir / "requires_review.md").as_posix(),
        (collision_risk_dir / "collision_risk_report.md").as_posix(),
        (collision_risk_dir / "unsafe_claims.md").as_posix(),
        *[ref for citation in citations for ref in citation.evidence_refs],
    ]

    return RelatedWorkDraftSkeleton(
        skeleton_id=skeleton_id,
        project_topic="VGGT / SMPL-X feature encoding",
        feed_forward_geometry=[
            "Start with feed-forward 3D geometry and VGGT context as background.",
            "Do not claim final novelty or absence of collision from fixture data.",
        ],
        human_prior_smplx=[
            "Frame the project as SMPL-X feature encoding for VGGT.",
            "Avoid presenting the route as direct SMPL-X replacement.",
        ],
        neural_body_sparse_voxel=[
            "Use NeuralBody as sparse voxel / structured latent inspiration only.",
            "Keep NeuralBody citation and collision status pending real paper review.",
        ],
        triplane_rasterized_pose_feature=[
            "Use HumanRAM as SMPL-X canonical / tri-plane / rasterized feature "
            "inspiration only.",
            "Keep HumanRAM citation and collision status pending real paper review.",
        ],
        vggt_human_extensions=[
            "Treat HART as potentially closer and requiring focused review.",
            "Treat VGGT-HPE, HGGT, and Fus3D as requires-real-paper-review items.",
        ],
        difference_from_our_route=[
            "Current route is SMPL-X feature encoding for VGGT.",
            "SparseConv3D remains planned / requires-real-experiment.",
            "This skeleton does not establish final related-work positioning.",
        ],
        requires_review_list=_bullet_lines(related_work_dir / "requires_review.md"),
        unsafe_claims_list=_bullet_lines(collision_risk_dir / "unsafe_claims.md"),
        citations=citations,
        citation_safety=citation_safety,
        evidence_refs=evidence_refs,
        requires_human_review=True,
    )


def render_related_work_skeleton(skeleton: RelatedWorkDraftSkeleton) -> str:
    """Render a related-work skeleton without final prose."""

    lines = [
        f"# Related Work Skeleton: {skeleton.project_topic}",
        "",
        "This is a draft skeleton, not camera-ready related-work text.",
        "",
        "## Feed-forward Geometry",
        "",
        *_bullets(skeleton.feed_forward_geometry),
        "",
        "## Human Prior / SMPL-X",
        "",
        *_bullets(skeleton.human_prior_smplx),
        "",
        "## Neural Body / Sparse Voxel",
        "",
        *_bullets(skeleton.neural_body_sparse_voxel),
        "",
        "## Tri-plane / Rasterized Pose Feature",
        "",
        *_bullets(skeleton.triplane_rasterized_pose_feature),
        "",
        "## VGGT Human Extensions",
        "",
        *_bullets(skeleton.vggt_human_extensions),
        "",
        "## Difference From Our Route",
        "",
        *_bullets(skeleton.difference_from_our_route),
        "",
        "## Citation Candidates",
        "",
        *_bullets(
            [
                f"`{citation.citation_id}` source_status=`{citation.source_status}`"
                for citation in skeleton.citations
            ]
        ),
        "",
        "## Requires Review",
        "",
        *_bullets(skeleton.requires_review_list),
        "",
        "## Unsafe Claims",
        "",
        *_bullets(skeleton.unsafe_claims_list),
        "",
        "## Evidence Refs",
        "",
        *_bullets([f"`{ref}`" for ref in skeleton.evidence_refs]),
        "",
        "## Boundary",
        "",
        "- No final related-work paragraph is generated.",
        "- No citation is fabricated.",
        "- Fixture digests are not citation-grade evidence.",
        "- Human review is required before paper claims.",
        "",
    ]
    return "\n".join(lines)


def render_related_work_citation_safety(
    skeleton: RelatedWorkDraftSkeleton,
) -> str:
    """Render citation safety for a related-work skeleton."""

    return render_citation_safety_report(skeleton.citation_safety)


def _bullet_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    bullets: list[str] = []
    current: str | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            if current is not None:
                bullets.append(current)
            current = stripped[2:]
        elif current is not None and stripped:
            current = f"{current} {stripped}"
    if current is not None:
        bullets.append(current)
    return bullets


def _bullets(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] or ["- Not specified."]
