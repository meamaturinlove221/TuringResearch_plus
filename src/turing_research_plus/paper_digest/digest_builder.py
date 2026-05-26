"""Build PaperDigest objects from local notes."""

from __future__ import annotations

import re

from turing_research_plus.paper_digest.models import (
    PaperDigest,
    PaperDigestInput,
    PaperDigestSourceStatus,
)
from turing_research_plus.paper_digest.three_pass import build_three_pass_notes


def build_paper_digest(request: PaperDigestInput) -> PaperDigest:
    """Build a conservative paper digest from local text or three-pass notes."""

    text = request.source_text or ""
    notes = request.pass_notes or build_three_pass_notes(text)
    requires_real_paper = request.source_status in {
        PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
        PaperDigestSourceStatus.REQUIRES_REAL_PAPER,
        PaperDigestSourceStatus.MANUAL_NOTE,
    }
    return PaperDigest(
        paper_id=request.paper_id,
        title=request.title,
        source_status=request.source_status,
        pass1_summary=notes.pass1_summary,
        pass2_notes=notes.pass2_notes,
        pass3_deep_notes=notes.pass3_deep_notes,
        method_contribution=_line_after(text, "method contribution")
        or _line_after(text, "core method")
        or "requires-real-paper-review",
        figures_to_inspect=_section_items(text, "key figures")
        or ["requires-real-paper-review figure list"],
        equations_to_inspect=_section_items(text, "equations to inspect")
        or ["requires-real-paper-review equation list"],
        experiment_table_notes=_section_items(text, "key tables")
        or _section_items(text, "experiment table notes")
        or ["requires-real-paper-review table list"],
        what_to_borrow=_section_items(text, "what to borrow")
        or ["Use as a comparison scaffold only after real paper review."],
        what_not_to_copy=_section_items(text, "what not to copy")
        or ["Do not copy implementation details, paper text, or unsupported claims."],
        collision_notes=_collision_notes(text),
        related_work_positioning=_related_work_notes(text),
        requires_human_review=True,
        requires_real_paper=requires_real_paper,
        human_verified=False,
        limitations=_limitations(request),
    )


def _section_items(text: str, heading: str) -> list[str]:
    pattern = re.compile(
        rf"^#+\s*{re.escape(heading)}\s*$([\s\S]*?)(?=^#+\s|\Z)",
        re.IGNORECASE | re.MULTILINE,
    )
    match = pattern.search(text)
    if not match:
        return []
    items: list[str] = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def _line_after(text: str, label: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(label)}:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(text)
    return None if match is None else match.group(1).strip()


def _collision_notes(text: str) -> list[str]:
    lowered = text.lower()
    notes: list[str] = []
    if "smpl" in lowered:
        notes.append("SMPL / SMPL-X overlap requires paper-level verification.")
    if "sparse" in lowered or "voxel" in lowered:
        notes.append("Sparse or voxel representation may overlap with VGGT human-prior route.")
    if "tri-plane" in lowered or "triplane" in lowered:
        notes.append("Tri-plane representation is a related comparison point, not a claim.")
    if "humanram" in lowered and not any("tri-plane" in note.lower() for note in notes):
        notes.append("HumanRAM tri-plane relevance requires real paper verification.")
    return notes or ["Collision risk requires real paper review."]


def _related_work_notes(text: str) -> list[str]:
    lowered = text.lower()
    notes: list[str] = []
    if "neuralbody" in lowered:
        notes.append("Use as body-prior / sparse-voxel related-work context.")
    if "humanram" in lowered:
        notes.append("Use as SMPL-X / tri-plane / rasterized-token related-work context.")
    return notes or ["Place in requires-review related-work bucket."]


def _limitations(request: PaperDigestInput) -> list[str]:
    limitations = [
        "Digest is a review scaffold, not a complete paper reading.",
        "Do not treat fixture content as citation-grade evidence.",
        "Requires human review before related-work claims.",
    ]
    if request.source_status == PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE:
        limitations.append("Source status is fake-or-manual-note.")
    if request.citation is None:
        limitations.append("No verified citation was provided.")
    return limitations
