import pytest

from turing_research_plus.architecture.models import (
    ArchitectureDiagramSpec,
    ArchitectureNode,
    ArchitectureSourceType,
)


def test_architecture_model_requires_valid_edges() -> None:
    with pytest.raises(ValueError, match="unknown nodes"):
        ArchitectureDiagramSpec(
            diagram_id="bad",
            title="Bad",
            source_type=ArchitectureSourceType.METHOD_CARD,
            source_ref="fixture",
            nodes=[ArchitectureNode(node_id="a", label="A")],
            edges=[{"source": "a", "target": "missing"}],
        )


def test_fixture_diagram_requires_human_review() -> None:
    with pytest.raises(ValueError, match="fixture-derived"):
        ArchitectureDiagramSpec(
            diagram_id="fixture",
            title="Fixture",
            source_type=ArchitectureSourceType.FIXTURE,
            source_ref="fixture",
            nodes=[ArchitectureNode(node_id="a", label="A")],
            requires_human_review=False,
        )
