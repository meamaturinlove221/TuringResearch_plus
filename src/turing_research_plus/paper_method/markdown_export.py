"""Markdown export for method cards."""

from __future__ import annotations

from turing_research_plus.paper_method.models import PaperMethodCard


def export_method_card_markdown(card: PaperMethodCard) -> str:
    """Render a PaperMethodCard as Markdown."""

    lines = [
        f"# Method Card: {card.title}",
        "",
        f"- Paper ID: `{card.paper_id}`",
        f"- Source type: `{card.source_type.value}`",
        f"- Requires human review: {str(card.requires_human_review).lower()}",
        f"- Collision risk: `{card.collision_risk.value}`",
        "",
        "## Task",
        "",
        card.task,
        "",
        "## Inputs",
        "",
        *_items(card.inputs),
        "",
        "## Outputs",
        "",
        *_items(card.outputs),
        "",
        "## Representation",
        "",
        *_items(card.representation),
        "",
        "## Core Method",
        "",
        card.core_method,
        "",
        "## Architecture Components",
        "",
        *_items(card.architecture_components),
        "",
        "## VGGT Mapping",
        "",
        f"- SMPL / SMPL-X role: {card.mapping_to_vggt.smpl_role}",
        f"- voxel / sparseconv relevance: {card.mapping_to_vggt.voxel_sparseconv_relevance}",
        f"- tri-plane relevance: {card.mapping_to_vggt.triplane_relevance}",
        f"- token alignment relevance: {card.mapping_to_vggt.token_alignment_relevance}",
        f"- geometry output relevance: {card.mapping_to_vggt.geometry_output_relevance}",
        (
            "- difference from VGGT objective: "
            f"{card.mapping_to_vggt.difference_from_vggt_objective}"
        ),
        f"- potential collision risk: {card.mapping_to_vggt.potential_collision_risk.value}",
        "",
        "## What To Borrow",
        "",
        *_items(card.what_to_borrow),
        "",
        "## What Not To Copy",
        "",
        *_items(card.what_not_to_copy),
        "",
        "## Limitations",
        "",
        *_items(card.limitations),
    ]
    return "\n".join(lines) + "\n"


def _items(items: list[str]) -> list[str]:
    return [f"- {item}" for item in items] if items else ["- none recorded"]
