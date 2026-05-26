"""Claim safety helpers for related-work positioning."""

from __future__ import annotations

from turing_research_plus.related_work.models import (
    MissingEvidenceItem,
    PaperGroup,
    PaperGroupEntry,
    PositioningClaim,
)


def build_safe_claims(groups: list[PaperGroupEntry]) -> list[PositioningClaim]:
    """Build conservative claims that remain suitable for review drafts."""

    claims = [
        PositioningClaim(
            text="The current direction should be framed as SMPL-X feature encoding for VGGT.",
            basis=(
                "Project route packs and dogfooding docs define feature encoding "
                "as the current direction."
            ),
            caveat="This does not establish novelty or experimental success.",
        ),
        PositioningClaim(
            text=(
                "NeuralBody and HumanRAM are useful comparison lenses for "
                "human-prior representations."
            ),
            basis="Method-card fixtures identify sparse voxel and tri-plane style representations.",
            caveat="Real paper review is required before final related-work wording.",
        ),
    ]
    if any(group.group == PaperGroup.NEURALBODY_SPARSE_VOXEL for group in groups):
        claims.append(
            PositioningClaim(
                text=(
                    "NeuralBody can be discussed as inspiration around SMPL structured "
                    "latent and sparse voxel ideas."
                ),
                basis=(
                    "Current fixtures map NeuralBody to structured latent / sparse "
                    "voxel concepts."
                ),
                caveat="Its target is not treated as VGGT point completion in current fixtures.",
            )
        )
    if any(group.group == PaperGroup.HUMANRAM_TRIPLANE_RASTER for group in groups):
        claims.append(
            PositioningClaim(
                text=(
                    "HumanRAM can be discussed as inspiration around SMPL-X canonical, "
                    "tri-plane, and rasterized token features."
                ),
                basis="Current fixtures map HumanRAM to tri-plane and rasterized pose features.",
                caveat=(
                    "Its output target differs from the current VGGT direction "
                    "in fixture evidence."
                ),
            )
        )
    return claims


def build_unsafe_claims() -> list[PositioningClaim]:
    """Build claims that should not be used yet."""

    return [
        PositioningClaim(
            text="The project has definitively no collision with existing papers.",
            basis="No real full-paper review has established this.",
            caveat="Use collision risk and manual review before making novelty claims.",
        ),
        PositioningClaim(
            text="The related work review is complete.",
            basis="Current examples use fake/manual fixtures and partial local artifacts.",
            caveat="Do not present fixture outputs as complete literature coverage.",
        ),
        PositioningClaim(
            text="SparseConv3D integration has succeeded.",
            basis="No evidence-ledger record establishes a real SparseConv3D success.",
            caveat=(
                "Keep SparseConv3D as planned or requires-real-experiment unless "
                "real evidence exists."
            ),
        ),
    ]


def build_missing_evidence(groups: list[PaperGroupEntry]) -> list[MissingEvidenceItem]:
    """Build missing evidence list."""

    items = [
        MissingEvidenceItem(
            item="citation-grade EvidenceRef for each positioning claim",
            reason="Fixture and fake graph outputs are not complete literature review.",
            required_action="Perform real paper review and attach evidence refs.",
        ),
        MissingEvidenceItem(
            item="key figures, tables, and method cards for close papers",
            reason="Positioning requires figure/table/method evidence before final claims.",
            required_action=(
                "Extract or manually summarize figures and tables for high-risk papers."
            ),
        ),
    ]
    close_titles = [
        group.title
        for group in groups
        if group.group
        in {
            PaperGroup.UNKNOWN_OR_REQUIRES_REVIEW,
            PaperGroup.VGGT_HUMAN_EXTENSIONS,
            PaperGroup.RECONSTRUCTION_OR_ANIMATION,
        }
    ]
    for title in close_titles:
        items.append(
            MissingEvidenceItem(
                item=title,
                reason="This paper may be close or is not sufficiently understood.",
                required_action="Perform focused human review before final positioning.",
            )
        )
    for title in ["HART", "VGGT-HPE", "HGGT", "Fus3D"]:
        if not any(title.lower() in group.title.lower() for group in groups):
            items.append(
                MissingEvidenceItem(
                    item=title,
                    reason=(
                        "VGGT-specific comparison requested but no complete reviewed card "
                        "exists."
                    ),
                    required_action="Create a reviewed method card before making claims.",
                )
            )
    return items
