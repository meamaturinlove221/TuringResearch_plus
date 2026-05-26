"""Map method-card evidence into VGGT relevance fields."""

from __future__ import annotations

from turing_research_plus.paper_method.models import CollisionRisk, VGGTMethodMapping


def map_to_vggt(text: str, representations: list[str]) -> VGGTMethodMapping:
    """Create a conservative VGGT mapping from local note text."""

    lowered = text.lower()
    has_smplx = "SMPL-X" in representations or "smpl-x" in lowered or "smplx" in lowered
    has_smpl = "SMPL" in representations or "smpl" in lowered
    has_sparse = any(item in representations for item in ["voxel", "sparse convolution"])
    has_triplane = "tri-plane" in representations
    has_token = "token" in representations
    has_geometry = "geometry" in representations or "general 3D geometry" in lowered

    collision = CollisionRisk.REQUIRES_REVIEW
    if has_smplx or has_sparse or has_triplane:
        collision = CollisionRisk.MEDIUM
    if has_token and has_geometry:
        collision = CollisionRisk.HIGH

    return VGGTMethodMapping(
        smpl_role=_role(has_smpl, has_smplx),
        voxel_sparseconv_relevance="relevant" if has_sparse else "not established in fixture",
        triplane_relevance="relevant" if has_triplane else "not established in fixture",
        token_alignment_relevance="relevant" if has_token else "not established in fixture",
        geometry_output_relevance="relevant" if has_geometry else "requires review",
        difference_from_vggt_objective=(
            "Fixture describes a human-specific method; VGGT objective remains general "
            "geometry unless evidence says otherwise."
        ),
        potential_collision_risk=collision,
    )


def _role(has_smpl: bool, has_smplx: bool) -> str:
    if has_smplx:
        return "SMPL-X appears as a body prior or feature source in the fixture note."
    if has_smpl:
        return "SMPL appears as a body prior or feature source in the fixture note."
    return "No SMPL / SMPL-X role is established by this fixture."
