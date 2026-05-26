"""Three-pass reading expansion for paper digests."""

from __future__ import annotations

import re

from turing_research_plus.paper_digest.models import ThreePassReadingNotes


def build_three_pass_notes(source_text: str) -> ThreePassReadingNotes:
    """Build conservative three-pass notes from local text."""

    title = _first_heading(source_text)
    key_terms = _key_terms(source_text)
    return ThreePassReadingNotes(
        pass1_summary=(
            f"Bird's-eye scan for {title}: task and contribution require real paper review."
        ),
        pass2_notes=[
            "Extract inputs, outputs, representation, and method mechanics from local note.",
            f"Detected review terms: {', '.join(key_terms) if key_terms else 'none'}",
            "Draft method-card fields only as review scaffolding.",
        ],
        pass3_deep_notes=[
            "Deep mechanics require checking original figures, equations, and experiments.",
            "Collision notes remain provisional until real paper review.",
            "VGGT mapping is a planning aid, not a final related-work claim.",
        ],
        requires_real_paper_review=True,
    )


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.strip("# ").strip() or "paper"
    return "paper"


def _key_terms(text: str) -> list[str]:
    lowered = text.lower()
    terms = [
        "SMPL-X",
        "SMPL",
        "voxel",
        "SparseConv3D",
        "tri-plane",
        "token",
        "geometry",
    ]
    return [term for term in terms if re.search(re.escape(term.lower()), lowered)]
