"""Deterministic caption generation for paper assets."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.paper.figure_registry import FigureAsset


class CaptionGenerateInput(BaseModel):
    """Input for paper.caption_generate."""

    model_config = ConfigDict(extra="forbid")

    asset: FigureAsset
    evidence_refs: list[EvidenceRef] = Field(default_factory=list)


class CaptionGenerateOutput(BaseModel):
    """Output for paper.caption_generate."""

    model_config = ConfigDict(extra="forbid")

    figure_id: str = Field(min_length=1)
    caption: str = Field(min_length=1)
    evidence_refs: list[EvidenceRef] = Field(min_length=1)


def generate_caption(input_data: CaptionGenerateInput) -> CaptionGenerateOutput:
    """Generate a deterministic evidence-backed caption."""

    evidence_refs = input_data.evidence_refs
    if not evidence_refs:
        raise ValueError("caption generation requires evidence_refs")
    caption = input_data.asset.caption or (
        f"{input_data.asset.title}. Source: {input_data.asset.source_file}."
    )
    return CaptionGenerateOutput(
        figure_id=input_data.asset.figure_id,
        caption=caption,
        evidence_refs=evidence_refs,
    )


def paper_caption_generate(input_data: CaptionGenerateInput) -> dict[str, object]:
    """Thin paper.caption_generate wrapper."""

    return generate_caption(input_data).model_dump(mode="json")
