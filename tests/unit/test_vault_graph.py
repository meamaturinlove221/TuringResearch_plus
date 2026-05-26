import pytest

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.vault.graph import DuplicateEdgeError
from turing_research_plus.vault.models import VaultEdge, VaultEdgeType, VaultEntityType, VaultPage
from turing_research_plus.vault.service import VaultService


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="source-1", locator="p.1", quote="Claim support.")


def test_add_edge_duplicate_rejected_and_traversal(tmp_path) -> None:
    service = VaultService(tmp_path)
    service.compile_page(
        VaultPage(page_id="claim-1", title="Claim", entity_type=VaultEntityType.CLAIM)
    )
    service.compile_page(
        VaultPage(page_id="evidence-1", title="Evidence", entity_type=VaultEntityType.EVIDENCE)
    )
    edge = VaultEdge(
        source_id="claim-1",
        target_id="evidence-1",
        edge_type=VaultEdgeType.SUPPORTED_BY,
        evidence=[evidence()],
    )

    service.add_edge(edge)

    with pytest.raises(DuplicateEdgeError):
        service.add_edge(edge)
    assert service.query_graph("claim-1") == ["evidence-1"]
    stats = service.graph_stats()
    assert stats.page_count == 2
    assert stats.edge_count == 1
    assert stats.orphan_count == 0
