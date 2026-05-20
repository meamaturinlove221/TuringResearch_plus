import pytest

from tuling_research_plus.artifacts.models import EvidenceRef
from tuling_research_plus.paper.caption_generator import (
    CaptionGenerateInput,
    generate_caption,
    paper_caption_generate,
)
from tuling_research_plus.paper.figure_registry import FigureAsset


def evidence() -> EvidenceRef:
    return EvidenceRef(
        source_id="experiment-report-1",
        locator="figure-1",
        quote="The figure reports experiment results.",
    )


def asset(caption: str | None = None) -> FigureAsset:
    return FigureAsset(
        figure_id="fig-1",
        title="Experiment Result",
        source_file="paper/figures/result.png",
        caption=caption or "Experiment result summary.",
        used_in_blocks=["experiments"],
    )


def test_caption_generate_uses_existing_caption() -> None:
    result = generate_caption(
        CaptionGenerateInput(
            asset=asset("Existing caption."),
            evidence_refs=[evidence()],
        )
    )

    assert result.caption == "Existing caption."
    assert result.evidence_refs[0].source_id == "experiment-report-1"


def test_caption_generate_requires_evidence() -> None:
    with pytest.raises(ValueError, match="caption generation requires evidence_refs"):
        generate_caption(CaptionGenerateInput(asset=asset(), evidence_refs=[]))


def test_paper_caption_generate_tool_returns_json_payload() -> None:
    payload = paper_caption_generate(
        CaptionGenerateInput(asset=asset(), evidence_refs=[evidence()])
    )

    assert payload["figure_id"] == "fig-1"
    assert payload["caption"] == "Experiment result summary."
