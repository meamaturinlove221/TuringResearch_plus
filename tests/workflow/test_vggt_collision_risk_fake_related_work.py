from __future__ import annotations

import json
from pathlib import Path

from turing_research_plus.collision.models import PaperComparisonInput
from turing_research_plus.collision.tools import collision_risk_detect
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType

ROOT = Path(__file__).resolve().parents[2]
EXAMPLE = ROOT / "examples" / "vggt-human-prior-survey"


def _fixture_cards() -> list[dict[str, object]]:
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


def test_vggt_collision_risk_uses_fake_related_work_conservatively() -> None:
    citation_graph = json.loads(
        (EXAMPLE / "citation_graph" / "fake_related_work_graph.json").read_text(
            encoding="utf-8"
        )
    )

    report = collision_risk_detect(
        PaperComparisonInput(compared_papers=_fixture_cards(), citation_graph=citation_graph)
    )

    assert report.requires_human_review is True
    assert report.risk_scores
    assert report.missing_evidence
    assert any("definitively no collision" in claim.text.lower() for claim in report.unsafe_claims)
    assert all("definitive no collision" not in claim.text.lower() for claim in report.safe_claims)
    assert any("SMPL-X feature encoding" in note for note in report.positioning_notes)


def test_collision_risk_example_outputs_exist() -> None:
    output = EXAMPLE / "collision_risk"

    assert (output / "overlap_matrix.csv").exists()
    assert "Requires human review" in (output / "collision_risk_report.md").read_text(
        encoding="utf-8"
    )
    assert "SparseConv3D integration is already successful" in (
        output / "unsafe_claims.md"
    ).read_text(encoding="utf-8")
