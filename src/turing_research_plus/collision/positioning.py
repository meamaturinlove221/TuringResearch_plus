"""Positioning notes for VGGT collision reports."""

from __future__ import annotations

from turing_research_plus.collision.models import RiskScore


def build_positioning_notes(risk_scores: list[RiskScore]) -> list[str]:
    """Return conservative VGGT-specific positioning notes."""

    notes = [
        "Current target is SMPL-X feature encoding for VGGT, not direct SMPL-X replacement.",
        "No definitive no-collision statement is allowed from fixture data.",
    ]
    for score in risk_scores:
        title = score.title.lower()
        if "neuralbody" in title:
            notes.append(
                "NeuralBody appears related through SMPL structured latent / sparseconv ideas, "
                "but its target is not VGGT point completion in current fixtures."
            )
        elif "humanram" in title:
            notes.append(
                "HumanRAM appears related through SMPL-X tri-plane / rasterized pose features, "
                "but target and output differ in current fixtures."
            )
        elif "hart" in title:
            notes.append("HART may be closer to human reconstruction and needs focused review.")
        elif "vggt-hpe" in title:
            notes.append(
                "VGGT-HPE may be lower risk if limited to head pose, but details require review."
            )
        elif "hggt" in title or "fus3d" in title:
            notes.append(f"{score.title} requires real paper review before positioning claims.")
    return list(dict.fromkeys(notes))
