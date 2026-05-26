import pytest

from turing_research_plus.paper_method.models import (
    CollisionRisk,
    PaperMethodCard,
    PaperMethodCardInput,
    PaperSourceType,
    VGGTMethodMapping,
)


def mapping() -> VGGTMethodMapping:
    return VGGTMethodMapping(
        smpl_role="requires review",
        voxel_sparseconv_relevance="requires review",
        triplane_relevance="requires review",
        token_alignment_relevance="requires review",
        geometry_output_relevance="requires review",
        difference_from_vggt_objective="requires review",
        potential_collision_risk=CollisionRisk.REQUIRES_REVIEW,
    )


def test_fake_manual_method_card_requires_human_review() -> None:
    with pytest.raises(ValueError, match="requires human review"):
        PaperMethodCard(
            paper_id="fixture",
            title="Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            task="test",
            core_method="test",
            training_objective="test",
            collision_risk=CollisionRisk.REQUIRES_REVIEW,
            mapping_to_vggt=mapping(),
            requires_human_review=False,
        )


def test_method_card_input_requires_exactly_one_source() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        PaperMethodCardInput(
            paper_id="p",
            title="Paper",
            source_type=PaperSourceType.MANUAL_NOTE,
        )
