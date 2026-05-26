from __future__ import annotations

from turing_research_plus.related_work.models import RelatedWorkPositioningInput
from turing_research_plus.related_work.positioning import build_related_work_positioning


def test_related_work_positioning_builds_conservative_report() -> None:
    report = build_related_work_positioning(
        RelatedWorkPositioningInput(
            method_cards=[
                {
                    "paper_id": "neuralbody",
                    "title": "NeuralBody",
                    "representation": ["SMPL structured latent", "sparse voxel"],
                }
            ],
            collision_report={
                "risk_scores": [
                    {"paper_id": "hart", "title": "HART requires-real-paper-review"}
                ]
            },
        )
    )

    assert report.requires_human_review is True
    assert report.paper_groups
    assert report.method_clusters
    assert any("SMPL-X feature encoding" in item for item in report.differentiation_points)
    assert any("HART" in item.item for item in report.missing_evidence)
    assert all("definitive no collision" not in claim.text.lower() for claim in report.safe_claims)
