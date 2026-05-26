"""Build evidence-linked method section skeletons."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

from turing_research_plus.paper_write.figure_linker import (
    MethodFigureLink,
    collect_mermaid_figure_links,
)


class MethodSectionSkeleton(BaseModel):
    """Review-only method section skeleton."""

    model_config = ConfigDict(extra="forbid")

    skeleton_id: str = Field(min_length=1)
    project_topic: str = Field(min_length=1)
    problem_setting: list[str] = Field(default_factory=list)
    overview: list[str] = Field(default_factory=list)
    smplx_feature_encoding: list[str] = Field(default_factory=list)
    vggt_integration: list[str] = Field(default_factory=list)
    route_variants: list[str] = Field(default_factory=list)
    hard_gates: list[str] = Field(default_factory=list)
    implementation_notes: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    figure_placeholders: list[MethodFigureLink] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)
    unsafe_claims: list[str] = Field(default_factory=list)
    requires_human_review: bool = True
    claims_experiment_verified: bool = False
    generated_final_contribution_claims: bool = False

    @model_validator(mode="after")
    def method_skeleton_stays_review_only(self) -> Self:
        if not self.requires_human_review:
            raise ValueError("method section skeleton requires human review")
        if self.claims_experiment_verified:
            raise ValueError("method section skeleton must not claim verification")
        if self.generated_final_contribution_claims:
            raise ValueError("method section skeleton must not generate final claims")
        if not self.evidence_refs:
            raise ValueError("method section skeleton must link evidence refs")
        if not self.figure_placeholders:
            raise ValueError("method section skeleton must include figure placeholders")
        if not self.limitations:
            raise ValueError("method section skeleton must include limitations")
        return self


def build_vggt_method_section_skeleton(
    method_cards_dir: Path,
    architecture_diagrams_dir: Path,
    route_specs_dir: Path,
    *,
    skeleton_id: str = "vggt_method_section_skeleton",
) -> MethodSectionSkeleton:
    """Build the VGGT method section skeleton from local fixture material."""

    method_card_paths = sorted(method_cards_dir.glob("*.md"))
    route_paths = sorted(route_specs_dir.glob("*.yaml"))
    figure_links = collect_mermaid_figure_links(architecture_diagrams_dir)
    route_summaries = [_route_summary(path) for path in route_paths]
    hard_gates = _collect_hard_gates(route_paths)
    evidence_refs = [
        *[path.as_posix() for path in method_card_paths],
        *[link.path for link in figure_links],
        *[path.as_posix() for path in route_paths],
    ]

    borrow_terms = _collect_section_bullets(method_card_paths, "What To Borrow")
    not_copy_terms = _collect_section_bullets(method_card_paths, "What Not To Copy")

    return MethodSectionSkeleton(
        skeleton_id=skeleton_id,
        project_topic="VGGT / SMPL-X Human Prior",
        problem_setting=[
            "Describe a human-prior route for VGGT without claiming completion.",
            "Treat method-card fixtures as comparison vocabulary and review inputs.",
        ],
        overview=[
            "Organize the method around SMPL-X feature encoding, VGGT integration, "
            "and route-gated validation.",
            "Use NeuralBody / HumanRAM fixture notes as inspiration only, not copied "
            "method claims.",
        ],
        smplx_feature_encoding=[
            "Represent SMPL-X as feature encodings rather than direct mesh output "
            "replacement.",
            "Candidate encodings include voxel, tri-plane, and token-aligned features; "
            "all remain evidence-gated.",
            *_prefix_items("Borrowable comparison terms", borrow_terms),
        ],
        vggt_integration=[
            "Place human-prior features at the VGGT token or point-residual interface "
            "as a planned architecture section.",
            "Separate adapter design from verified experiment outputs.",
        ],
        route_variants=route_summaries,
        hard_gates=hard_gates,
        implementation_notes=[
            "Implementation notes are derived from route DSL and architecture "
            "diagrams.",
            "No Modal or VGGT execution is represented by this section skeleton.",
            *_prefix_items("Do not copy", not_copy_terms),
        ],
        limitations=[
            "Architecture diagrams are derived from fixtures and require human review.",
            "Method cards require real paper review before citation-grade use.",
            "SparseConv3D backend success is not established by this skeleton.",
            "Experiment evidence is missing, so results wording must remain blocked.",
        ],
        figure_placeholders=figure_links,
        evidence_refs=evidence_refs,
        unsafe_claims=[
            "Do not claim the method is fully experimentally verified.",
            "Do not claim SparseConv3D success.",
            "Do not claim final contribution over related work.",
            "Do not fabricate figures, tables, metrics, or ablation results.",
        ],
        requires_human_review=True,
    )


def _collect_section_bullets(paths: list[Path], heading: str) -> list[str]:
    bullets: list[str] = []
    for path in paths:
        lines = path.read_text(encoding="utf-8").splitlines()
        in_section = False
        for line in lines:
            stripped = line.strip()
            if stripped == f"## {heading}":
                in_section = True
                continue
            if in_section and stripped.startswith("## "):
                break
            if in_section and stripped.startswith("- "):
                bullets.append(stripped[2:])
    return bullets


def _route_summary(path: Path) -> str:
    payload = _read_route_payload(path)
    route_id = payload.get("route_id", path.stem)
    status = payload.get("status", "unknown")
    final_states = ", ".join(payload.get("final_states", []))
    return (
        f"`{route_id}`: `{status}`; final states remain "
        f"{final_states or 'requires-human-review'}."
    )


def _collect_hard_gates(paths: list[Path]) -> list[str]:
    gates: list[str] = []
    for path in paths:
        payload = _read_route_payload(path)
        for gate in payload.get("hard_gates", []):
            gates.append(f"`{gate}` must pass before method/result promotion.")
    return gates


def _read_route_payload(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {"route_id": path.stem, "status": "requires-human-review"}
    return payload if isinstance(payload, dict) else {}


def _prefix_items(prefix: str, items: list[str]) -> list[str]:
    return [f"{prefix}: {item}" for item in items]
