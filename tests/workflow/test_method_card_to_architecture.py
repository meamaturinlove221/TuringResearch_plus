from pathlib import Path

from turing_research_plus.architecture.graph_builder import build_architecture_from_method_card
from turing_research_plus.architecture.markdown_export import export_architecture_markdown
from turing_research_plus.architecture.mermaid_export import export_architecture_mermaid
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType


def test_method_card_to_architecture_for_neuralbody_fixture() -> None:
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
    spec = build_architecture_from_method_card(card)
    mermaid = export_architecture_mermaid(spec)
    markdown = export_architecture_markdown(spec)

    assert "flowchart TB" in mermaid
    assert "requires-human-review" in mermaid
    assert "derived-from-fixture" in " ".join(spec.limitations)
    assert "```mermaid" in markdown


def test_method_card_to_architecture_for_humanram_fixture() -> None:
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
    spec = build_architecture_from_method_card(card)

    assert spec.requires_human_review is True
    assert any("tri-plane" in note for note in spec.mapping_notes)
