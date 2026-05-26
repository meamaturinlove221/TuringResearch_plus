from turing_research_plus.paper_method.mapping import map_to_vggt
from turing_research_plus.paper_method.models import CollisionRisk


def test_mapping_detects_smplx_sparseconv_relevance() -> None:
    mapping = map_to_vggt("SMPL-X sparseconv geometry note", ["SMPL-X", "sparse convolution"])

    assert "SMPL-X" in mapping.smpl_role
    assert mapping.voxel_sparseconv_relevance == "relevant"
    assert mapping.potential_collision_risk in {CollisionRisk.MEDIUM, CollisionRisk.HIGH}


def test_mapping_remains_review_when_no_signal() -> None:
    mapping = map_to_vggt("generic note", [])

    assert mapping.potential_collision_risk == CollisionRisk.REQUIRES_REVIEW
    assert "No SMPL" in mapping.smpl_role
