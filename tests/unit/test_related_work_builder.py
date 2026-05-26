from __future__ import annotations

from pathlib import Path

import pytest

from turing_research_plus.paper_write.related_work_builder import (
    RelatedWorkDraftSkeleton,
    build_vggt_related_work_draft_skeleton,
    render_related_work_citation_safety,
    render_related_work_skeleton,
)

ROOT = Path(__file__).resolve().parents[2]
VGGT = ROOT / "examples" / "vggt-human-prior-survey"


def _skeleton() -> RelatedWorkDraftSkeleton:
    return build_vggt_related_work_draft_skeleton(
        VGGT / "related_work",
        VGGT / "collision_risk",
        VGGT / "paper_digest",
    )


def test_related_work_draft_skeleton_contains_required_sections() -> None:
    skeleton = _skeleton()

    assert skeleton.feed_forward_geometry
    assert skeleton.human_prior_smplx
    assert skeleton.neural_body_sparse_voxel
    assert skeleton.triplane_rasterized_pose_feature
    assert skeleton.vggt_human_extensions
    assert skeleton.difference_from_our_route
    assert skeleton.requires_review_list
    assert skeleton.unsafe_claims_list
    assert skeleton.requires_human_review is True


def test_related_work_draft_citations_all_have_source_status() -> None:
    skeleton = _skeleton()
    statuses = {citation.citation_id: citation.source_status for citation in skeleton.citations}

    assert statuses["neuralbody-fixture"] == "fake-or-manual-note"
    assert statuses["humanram-fixture"] == "fake-or-manual-note"
    assert statuses["hart-review-needed"] == "requires-real-paper-review"
    assert all(citation.requires_human_review for citation in skeleton.citations)
    assert all(not citation.citation_grade for citation in skeleton.citations)


def test_related_work_draft_keeps_unsafe_claims_and_review_list() -> None:
    skeleton = _skeleton()
    review_text = "\n".join(skeleton.requires_review_list)
    unsafe_text = "\n".join(skeleton.unsafe_claims_list)

    assert "HART" in review_text
    assert "Fus3D" in review_text
    assert "citation-grade evidence" in review_text
    assert "related work has been completely reviewed" in unsafe_text
    assert "SparseConv3D integration is already successful" in unsafe_text


def test_related_work_draft_rejects_camera_ready_generation() -> None:
    payload = _skeleton().model_dump(mode="python")
    payload["generated_camera_ready_text"] = True

    with pytest.raises(ValueError, match="camera-ready text"):
        RelatedWorkDraftSkeleton(**payload)


def test_related_work_draft_markdown_exports_boundaries() -> None:
    skeleton = _skeleton()

    draft = render_related_work_skeleton(skeleton)
    safety = render_related_work_citation_safety(skeleton)

    assert "## Feed-forward Geometry" in draft
    assert "source_status=`fake-or-manual-note`" in draft
    assert "No final related-work paragraph is generated." in draft
    assert "Fake fixtures are not final citations." in safety
    assert "No citation is fabricated." in safety
