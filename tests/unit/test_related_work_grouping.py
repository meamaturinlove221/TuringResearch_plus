from __future__ import annotations

from turing_research_plus.related_work.grouping import classify_paper, group_method_cards
from turing_research_plus.related_work.models import PaperGroup


def test_group_method_cards_classifies_neuralbody_and_humanram() -> None:
    groups = group_method_cards(
        [
            {
                "paper_id": "neuralbody",
                "title": "NeuralBody",
                "representation": ["SMPL structured latent", "sparse voxel"],
            },
            {
                "paper_id": "humanram",
                "title": "HumanRAM",
                "representation": ["SMPL-X canonical", "tri-plane"],
            },
        ]
    )

    assert groups[0].group == PaperGroup.NEURALBODY_SPARSE_VOXEL
    assert groups[1].group == PaperGroup.HUMANRAM_TRIPLANE_RASTER
    assert all(group.requires_real_paper_review for group in groups)


def test_classify_unknown_requires_review() -> None:
    group, rationale = classify_paper("Unknown", "unclear")

    assert group == PaperGroup.UNKNOWN_OR_REQUIRES_REVIEW
    assert "Insufficient evidence" in rationale
