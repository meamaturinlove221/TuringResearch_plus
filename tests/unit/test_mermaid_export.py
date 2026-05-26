from turing_research_plus.architecture.mermaid_export import export_architecture_mermaid
from turing_research_plus.architecture.models import (
    ArchitectureDiagramSpec,
    ArchitectureEdge,
    ArchitectureGroup,
    ArchitectureNode,
    ArchitectureSourceType,
)
from turing_research_plus.sop.mermaid_export import export_mermaid, export_sop_markdown
from turing_research_plus.sop.models import (
    SOPEdge,
    SOPGraph,
    SOPGraphType,
    SOPNode,
    SOPNodeKind,
)


def graph() -> SOPGraph:
    return SOPGraph(
        graph_id="test-graph",
        graph_type=SOPGraphType.PAPER,
        title="Test Graph",
        nodes=[
            SOPNode(node_id="input", label="Input", kind=SOPNodeKind.ARTIFACT),
            SOPNode(node_id="tool", label="paper.sop_graph_generate", kind=SOPNodeKind.TOOL),
            SOPNode(node_id="quality", label="EvidenceRef Gate", kind=SOPNodeKind.QUALITY_GATE),
            SOPNode(node_id="failure", label="Missing Evidence", kind=SOPNodeKind.FAILURE_GATE),
        ],
        edges=[
            SOPEdge(source="input", target="tool"),
            SOPEdge(source="tool", target="quality"),
            SOPEdge(source="quality", target="failure", label="failed"),
        ],
        input_artifacts=["ResearchBrief"],
        output_artifacts=["SOPGraph"],
        tools=["paper.sop_graph_generate"],
        quality_gates=["EvidenceRef Gate"],
        failure_gates=["Missing Evidence"],
    )


def test_mermaid_export_renders_valid_flowchart_text() -> None:
    mermaid = export_mermaid(graph())

    assert mermaid.startswith("flowchart TD")
    assert 'input[("Input")]' in mermaid
    assert "quality -- failed --> failure" in mermaid


def test_sop_markdown_contains_graph_and_gates() -> None:
    mermaid = export_mermaid(graph())
    markdown = export_sop_markdown(graph(), mermaid)

    assert "# TuringResearch Plus SOP: Test Graph" in markdown
    assert "```mermaid" in markdown
    assert "EvidenceRef Gate" in markdown
    assert "Missing Evidence" in markdown


def test_architecture_mermaid_export_supports_flowchart_tb_and_subgraph() -> None:
    spec = ArchitectureDiagramSpec(
        diagram_id="arch",
        title="Architecture",
        source_type=ArchitectureSourceType.METHOD_CARD,
        source_ref="fixture",
        nodes=[
            ArchitectureNode(node_id="a", label="A", group="Group One"),
            ArchitectureNode(node_id="b", label="B", group="Group One"),
        ],
        edges=[ArchitectureEdge(source="a", target="b", label="flows")],
        groups=[ArchitectureGroup(group_id="group_one", label="Group One")],
    )

    mermaid = export_architecture_mermaid(spec)

    assert mermaid.startswith("flowchart TB")
    assert "subgraph group_one[Group One]" in mermaid
    assert "a -- flows --> b" in mermaid
