from __future__ import annotations

import pytest

from turing_research_plus.cross_project.models import (
    CrossProjectEdge,
    CrossProjectEdgeType,
    CrossProjectEvidenceGraph,
    CrossProjectNode,
    CrossProjectNodeType,
)


def test_cross_project_graph_requires_human_review() -> None:
    with pytest.raises(ValueError, match="require human review"):
        CrossProjectEvidenceGraph(workspace_id="demo", requires_human_review=False)


def test_cross_project_node_is_not_evidence_source() -> None:
    with pytest.raises(ValueError, match="not evidence sources"):
        CrossProjectNode(
            node_id="claim:demo:1",
            label="No observed evidence",
            node_type=CrossProjectNodeType.CLAIM,
            evidence_source=True,
        )


def test_cross_project_edge_cannot_transfer_evidence() -> None:
    with pytest.raises(ValueError, match="cannot transfer evidence"):
        CrossProjectEdge(
            source_id="claim:a",
            target_id="claim:b",
            edge_type=CrossProjectEdgeType.RELATED_PROJECT,
            rationale="unsafe proof transfer",
            evidence_transfer=True,
        )
