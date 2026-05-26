from __future__ import annotations

from turing_research_plus.adapters.fake import FakeSemanticScholarAdapter
from turing_research_plus.adapters.models import (
    SemanticScholarAuthorLookup,
    SemanticScholarPaperBatchLookup,
    SemanticScholarPaperIdLookup,
    SemanticScholarPaperListLookup,
    SemanticScholarPaperLookup,
    SemanticScholarRecommendationLookup,
)
from turing_research_plus.semantic_graph.live_service import SemanticScholarLiveGraphService


def test_fake_adapter_supports_lookup_batch_and_lists() -> None:
    adapter = FakeSemanticScholarAdapter()

    lookup = adapter.paper_lookup(SemanticScholarPaperLookup(query="SparseConv3D", limit=1))
    by_id = adapter.paper_lookup_by_id(SemanticScholarPaperIdLookup(paper_id="S2-1"))
    batch = adapter.paper_batch(SemanticScholarPaperBatchLookup(paper_ids=["S2-1", "S2-2"]))
    refs = adapter.references(SemanticScholarPaperListLookup(paper_id="S2-1", limit=2))
    cites = adapter.citations(SemanticScholarPaperListLookup(paper_id="S2-1", limit=2))
    recs = adapter.recommendations(
        SemanticScholarRecommendationLookup(paper_ids=["S2-1"], limit=2)
    )
    author = adapter.author(SemanticScholarAuthorLookup(author_id="A1"))

    assert lookup.papers[0]["title"] == "Fake result for SparseConv3D"
    assert by_id.papers[0]["paperId"] == "S2-1"
    assert len(batch.papers) == 2
    assert len(refs.papers) == 2
    assert len(cites.papers) == 2
    assert len(recs.papers) == 2
    assert author.authors[0]["authorId"] == "A1"
    assert lookup.source_metadata[0].human_verified is False


def test_fake_adapter_bridges_to_semantic_graph_models() -> None:
    service = SemanticScholarLiveGraphService(FakeSemanticScholarAdapter())

    result = service.paper_lookup_by_id("S2-1")

    assert result.status == "ok"
    assert result.paper is not None
    assert result.paper.paper_id == "S2-1"
    assert result.paper.metadata["human_verified"] is False
