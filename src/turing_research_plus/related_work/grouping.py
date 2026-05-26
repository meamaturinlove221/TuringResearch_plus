"""Group papers into conservative related-work buckets."""

from __future__ import annotations

from turing_research_plus.related_work.models import PaperGroup, PaperGroupEntry


def group_method_cards(method_cards: list[dict[str, object]]) -> list[PaperGroupEntry]:
    """Assign method-card-like records to related-work groups."""

    groups: list[PaperGroupEntry] = []
    for card in method_cards:
        paper_id = str(card.get("paper_id") or card.get("id") or card.get("title") or "unknown")
        title = str(card.get("title") or paper_id)
        text = _card_text(card)
        group, rationale = classify_paper(title, text)
        groups.append(
            PaperGroupEntry(
                paper_id=paper_id,
                title=title,
                group=group,
                rationale=rationale,
                requires_real_paper_review=True,
            )
        )
    return groups


def classify_paper(title: str, text: str) -> tuple[PaperGroup, str]:
    """Return a conservative group and rationale."""

    blob = f"{title} {text}".lower()
    if "neuralbody" in blob or ("sparse" in blob and "voxel" in blob):
        return (
            PaperGroup.NEURALBODY_SPARSE_VOXEL,
            "SMPL structured latent / sparse voxel ideas are relevant, but target differs.",
        )
    if "humanram" in blob or "tri-plane" in blob or "triplane" in blob:
        return (
            PaperGroup.HUMANRAM_TRIPLANE_RASTER,
            "SMPL-X canonical / tri-plane / rasterized feature ideas are relevant.",
        )
    if "smpl-x" in blob or "smpl" in blob:
        return (
            PaperGroup.SMPL_SMPLX_ENCODING,
            "Uses SMPL or SMPL-X representation and needs mapping review.",
        )
    if "vggt" in blob or "hpe" in blob or "human extension" in blob:
        return (
            PaperGroup.VGGT_HUMAN_EXTENSIONS,
            "Potentially related to VGGT human extension and must be reviewed.",
        )
    if "sparseconv" in blob or "minkowski" in blob or "torchsparse" in blob:
        return (
            PaperGroup.SPARSECONV_BACKENDS,
            "Sparse backend relevance is implementation-level, not novelty proof.",
        )
    if "reconstruction" in blob or "animation" in blob:
        return (
            PaperGroup.RECONSTRUCTION_OR_ANIMATION,
            "Human reconstruction or animation target may overlap partially.",
        )
    return (
        PaperGroup.UNKNOWN_OR_REQUIRES_REVIEW,
        "Insufficient evidence for confident grouping.",
    )


def _card_text(card: dict[str, object]) -> str:
    parts: list[str] = []
    for value in card.values():
        if isinstance(value, str):
            parts.append(value)
        elif isinstance(value, list):
            parts.extend(str(item) for item in value)
        elif isinstance(value, dict):
            parts.extend(str(item) for item in value.values())
    return " ".join(parts)
