from turing_research_plus.artifacts.models import ArtifactKind, EvidenceRef, ResearchArtifact
from turing_research_plus.vault.models import VaultEntityType
from turing_research_plus.vault.service import VaultService


def test_artifact_ingestion_creates_claim_and_evidence_pages(tmp_path) -> None:
    artifact = ResearchArtifact(
        artifact_id="artifact-1",
        kind=ArtifactKind.NOTE,
        title="Evidence-backed claim",
        created_by="unit-test",
        content={"claim": "Vaults preserve evidence."},
        evidence=[
            EvidenceRef(
                source_id="source-1",
                locator="section-1",
                quote="Vaults preserve evidence.",
            )
        ],
    )
    service = VaultService(tmp_path)

    result = service.ingest_artifact(artifact)

    assert [page.entity_type for page in result.pages] == [
        VaultEntityType.CLAIM,
        VaultEntityType.EVIDENCE,
    ]
    assert result.edges[0].source_id == "claim-artifact-1"
    assert result.edges[0].target_id == "evidence-artifact-1-1"
    assert service.read_page("claim-artifact-1").artifact_id == "artifact-1"


def test_search_page(tmp_path) -> None:
    service = VaultService(tmp_path)
    service.ingest_source(
        page_id="source-1",
        title="Semantic Graph Memory",
        body="Typed graph edges help memory retrieval.",
        evidence=[
            EvidenceRef(
                source_id="source-1",
                locator="body",
                quote="Typed graph edges help memory retrieval.",
            )
        ],
    )

    hits = service.search("graph memory")

    assert hits[0].page_id == "source-1"
    assert hits[0].score > 0
