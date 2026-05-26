from turing_research_plus.architecture.graphviz_export import export_architecture_graphviz
from turing_research_plus.architecture.models import (
    ArchitectureDiagramSpec,
    ArchitectureEdge,
    ArchitectureNode,
    ArchitectureSourceType,
)


def test_graphviz_export_renders_dot() -> None:
    spec = ArchitectureDiagramSpec(
        diagram_id="test",
        title="Test",
        source_type=ArchitectureSourceType.METHOD_CARD,
        source_ref="fixture",
        nodes=[
            ArchitectureNode(node_id="a", label="A"),
            ArchitectureNode(node_id="b", label="B"),
        ],
        edges=[ArchitectureEdge(source="a", target="b", label="flows")],
    )

    dot = export_architecture_graphviz(spec)

    assert dot.startswith('digraph "test"')
    assert '"a" -> "b" [label="flows"];' in dot
