from pathlib import Path

from turing_research_plus.architecture.graph_builder import (
    build_architecture_from_method_card,
    build_architecture_from_route,
)
from turing_research_plus.experiment_route.parser import parse_experiment_route
from turing_research_plus.paper_method.extractor import extract_paper_method_card
from turing_research_plus.paper_method.models import PaperMethodCardInput, PaperSourceType


def method_card_fixture() -> Path:
    return Path("examples/vggt-human-prior-survey/paper_method_cards/neuralbody.fixture.md")


def route_fixture() -> Path:
    return Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")


def test_build_architecture_from_method_card() -> None:
    card = extract_paper_method_card(
        PaperMethodCardInput(
            paper_id="neuralbody-fixture",
            title="NeuralBody Fixture",
            source_type=PaperSourceType.FAKE_OR_MANUAL_NOTE,
            source_path=method_card_fixture(),
        )
    )

    spec = build_architecture_from_method_card(card)

    assert spec.nodes
    assert spec.edges
    assert spec.requires_human_review is True
    assert any("SMPL" in note for note in spec.mapping_notes)


def test_build_architecture_from_route() -> None:
    route = parse_experiment_route(route_fixture())
    spec = build_architecture_from_route(route)

    assert spec.source_ref == "modal_sparseconv_v0"
    assert [node.label for node in spec.nodes][0] == "Preflight evidence check"
    assert any("not executed" in limitation for limitation in spec.limitations)
