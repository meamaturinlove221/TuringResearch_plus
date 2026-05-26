from pathlib import Path

from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.markdown_export import export_method_card_markdown
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType


def test_humanram_fixture_extracts_review_only_method_card() -> None:
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="humanram-fixture",
            title="HumanRAM Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=Path(
                "examples/vggt-human-prior-survey/paper_method_cards/humanram.fixture.md"
            ),
        )
    )
    markdown = export_method_card_markdown(card)

    assert card.requires_human_review is True
    assert card.mapping_to_vggt.geometry_output_relevance == "relevant"
    assert "feature encoding" in " ".join(card.what_to_borrow)
    assert "complete paper reading" in " ".join(card.limitations)
    assert "VGGT Mapping" in markdown
