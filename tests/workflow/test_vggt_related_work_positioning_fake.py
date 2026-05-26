from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.collision.models import PaperComparisonInput
from turing_research_plus.collision.tools import collision_risk_detect
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType
from turing_research_plus.related_work.markdown_export import (
    export_related_work_positioning_markdown,
)
from turing_research_plus.related_work.models import RelatedWorkPositioningInput
from turing_research_plus.related_work.tools import related_work_position

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"


def _cards() -> list[dict[str, object]]:
    cards: list[dict[str, object]] = []
    for path in sorted((EXAMPLE / "paper_method_cards").glob("*.fixture.md")):
        card = extract_paper_method_card(
            PaperMethodCardInput(
                paper_id=path.stem.replace(".fixture", ""),
                title=path.stem.replace(".fixture", "").title(),
                source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
                source_path=path,
            )
        )
        cards.append(card.model_dump(mode="json"))
    return cards


def test_vggt_related_work_positioning_fake_is_conservative() -> None:
    citation_graph = json.loads(
        (EXAMPLE / "citation_graph" / "fake_related_work_graph.json").read_text(
            encoding="utf-8"
        )
    )
    cards = _cards()
    collision = collision_risk_detect(
        PaperComparisonInput(compared_papers=cards, citation_graph=citation_graph)
    )

    report = related_work_position(
        RelatedWorkPositioningInput(
            method_cards=cards,
            citation_graph=citation_graph,
            collision_report=collision.model_dump(mode="json"),
        )
    )
    markdown = export_related_work_positioning_markdown(report)

    assert report.requires_human_review is True
    assert report.safe_claims
    assert report.unsafe_claims
    assert any(
        "SparseConv3D integration has succeeded" in claim.text
        for claim in report.unsafe_claims
    )
    assert any("HumanRAM" in claim.text for claim in report.safe_claims)
    assert "Related Work Positioning Report" in markdown


def test_related_work_example_outputs_exist() -> None:
    output = EXAMPLE / "related_work"

    assert "SMPL-X feature encoding" in (output / "related_work_positioning.md").read_text(
        encoding="utf-8"
    )
    assert "Current fixture outputs" in (output / "safe_related_work_claims.md").read_text(
        encoding="utf-8"
    )
    assert "HART" in (output / "requires_review.md").read_text(encoding="utf-8")
