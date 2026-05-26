"""Lightweight Paper-to-Method Card extractor."""

from __future__ import annotations

import re

from turing_research_plus.paper_method.mapping import map_to_vggt
from turing_research_plus.paper_method.models import (
    CollisionRisk,
    PaperMethodCard,
    PaperMethodCardInput,
    PaperSourceType,
)
from turing_research_plus.paper_method.taxonomy import (
    ARCHITECTURE_KEYWORDS,
    REPRESENTATION_KEYWORDS,
    TASK_KEYWORDS,
    labels_for_text,
)


def extract_paper_method_card(request: PaperMethodCardInput) -> PaperMethodCard:
    """Extract a conservative method card from local text or fixture notes."""

    text = _source_text(request)
    representations = labels_for_text(text, REPRESENTATION_KEYWORDS)
    architecture = labels_for_text(text, ARCHITECTURE_KEYWORDS)
    task_labels = labels_for_text(text, TASK_KEYWORDS)
    figures = _section_items(text, "key figures")
    tables = _section_items(text, "key tables")
    inputs = _section_items(text, "inputs") or _fallback_items(
        text,
        ["image", "video", "pose", "smpl"],
    )
    outputs = _section_items(text, "outputs") or _fallback_items(
        text,
        ["mesh", "radiance", "geometry"],
    )
    borrow = _section_items(text, "what to borrow") or [
        "Use as a structured comparison point only after real paper review."
    ]
    not_copy = _section_items(text, "what not to copy") or [
        "Do not copy implementation details or paper text from fixture notes."
    ]
    limitations = _limitations(request, text)
    mapping = map_to_vggt(text, representations)
    return PaperMethodCard(
        paper_id=request.paper_id,
        title=request.title,
        source_type=request.source_type,
        task=", ".join(task_labels) if task_labels else "requires-real-paper-review",
        inputs=inputs,
        outputs=outputs,
        representation=representations or ["requires-real-paper-review"],
        core_method=_core_method(text),
        architecture_components=architecture or ["requires-real-paper-review"],
        training_objective=_line_after(text, "training objective")
        or "requires-real-paper-review",
        inference_pipeline=_section_items(text, "inference pipeline")
        or ["requires-real-paper-review"],
        key_figures=figures,
        key_tables=tables,
        what_to_borrow=borrow,
        what_not_to_copy=not_copy,
        collision_risk=mapping.potential_collision_risk
        if mapping.potential_collision_risk != CollisionRisk.LOW
        else CollisionRisk.REQUIRES_REVIEW,
        mapping_to_vggt=mapping,
        evidence_refs=request.evidence_refs,
        limitations=limitations,
        requires_human_review=True
        if request.requires_real_paper_review
        or request.source_type == PaperSourceType.FAKE_OR_MANUAL_NOTE
        else not request.evidence_refs,
    )


def _source_text(request: PaperMethodCardInput) -> str:
    if request.source_text is not None:
        return request.source_text
    if request.source_path is None:
        raise ValueError("source_path is required when source_text is absent")
    return request.source_path.read_text(encoding="utf-8")


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


def _fallback_items(text: str, keywords: list[str]) -> list[str]:
    lowered = text.lower()
    return [keyword for keyword in keywords if keyword in lowered]


def _core_method(text: str) -> str:
    explicit = _line_after(text, "core method")
    if explicit:
        return explicit
    first_non_empty = next(
        (line.strip("# ").strip() for line in text.splitlines() if line.strip()),
        "",
    )
    return first_non_empty or "requires-real-paper-review"


def _limitations(request: PaperMethodCardInput, text: str) -> list[str]:
    limitations = _section_items(text, "limitations")
    limitations.append("Fixture is fake-or-manual-note / requires-real-paper-review.")
    if not request.evidence_refs:
        limitations.append("No citation-grade EvidenceRef is present.")
    if request.source_type == PaperSourceType.FAKE_OR_MANUAL_NOTE:
        limitations.append("This fixture does not prove complete paper reading.")
    return list(dict.fromkeys(limitations))
