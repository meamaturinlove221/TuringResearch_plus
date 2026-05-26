from pathlib import Path

from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.markdown_export import export_method_card_markdown
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType


def test_neuralbody_fixture_extracts_review_only_method_card() -> None:
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=Path(
                "examples/vggt-human-prior-survey/paper_method_cards/neuralbody.fixture.md"
            ),
        )
    )
    markdown = export_method_card_markdown(card)

    assert card.requires_human_review is True
    assert card.source_type == PaperSourceType.FAKE_OR_MANUAL_NOTE
    assert "requires real paper review" in " ".join(card.limitations).lower()
    assert "SMPL" in card.mapping_to_vggt.smpl_role
    assert "# Method Card" in markdown
