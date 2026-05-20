from tuling_research_plus.sop.mermaid_export import export_mermaid, export_sop_markdown
from tuling_research_plus.sop.models import (
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

    assert "# TulingResearch Plus SOP: Test Graph" in markdown
    assert "```mermaid" in markdown
    assert "EvidenceRef Gate" in markdown
    assert "Missing Evidence" in markdown
