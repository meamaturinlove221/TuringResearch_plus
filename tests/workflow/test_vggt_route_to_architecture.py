from pathlib import Path

from turing_research_plus.architecture.graph_builder import build_architecture_from_route
from turing_research_plus.architecture.graphviz_export import export_architecture_graphviz
from turing_research_plus.architecture.mermaid_export import export_architecture_mermaid
from turing_research_plus.experiment_route.parser import parse_experiment_route


def test_vggt_route_to_architecture_keeps_planned_boundary() -> None:
    route = parse_experiment_route(
        Path("examples/vggt-human-prior-survey/route_specs/modal_sparseconv_v0.yaml")
    )
    spec = build_architecture_from_route(route)
    mermaid = export_architecture_mermaid(spec)
    dot = export_architecture_graphviz(spec)

    assert spec.requires_human_review is True
    assert "not executed by TuringResearch" in spec.limitations
    assert "flowchart TB" in mermaid
    assert "Sparse backend probe planning" in mermaid
    assert any("Derived from Experiment Route DSL" in note for note in spec.mapping_notes)
    assert dot.startswith('digraph "modal_sparseconv_v0_architecture"')
