from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType


def test_extract_method_card_from_manual_note() -> None:
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="fixture",
            title="Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_text=(
                "# Fixture\n"
                "core method: SMPL-X sparseconv feature encoder.\n"
                "training objective: requires-real-paper-review.\n"
                "## Inputs\n- image\n"
                "## Outputs\n- geometry\n"
            ),
        )
    )

    assert card.paper_id == "fixture"
    assert card.requires_human_review is True
    assert "sparse convolution" in card.representation
    assert card.limitations


def test_extract_method_card_does_not_fabricate_missing_components() -> None:
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="empty",
            title="Empty",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_text="# Empty\n",
        )
    )

    assert card.representation == ["requires-real-paper-review"]
    assert card.training_objective == "requires-real-paper-review"
    assert card.requires_human_review is True
