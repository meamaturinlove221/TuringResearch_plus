import pytest
from pydantic import ValidationError

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.vault.models import VaultEdge, VaultEdgeType, VaultEntityType, VaultPage


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="source-1", locator="p.1", quote="Evidence quote.")


def test_vault_page_model() -> None:
    page = VaultPage(
        page_id="claim-1",
        title="Claim One",
        entity_type=VaultEntityType.CLAIM,
        evidence=[evidence()],
    )

    assert page.filename == "claim-1.md"
    assert page.entity_type == VaultEntityType.CLAIM


def test_supported_by_edge_requires_evidence() -> None:
    with pytest.raises(ValidationError):
        VaultEdge(
            source_id="claim-1",
            target_id="evidence-1",
            edge_type=VaultEdgeType.SUPPORTED_BY,
        )
