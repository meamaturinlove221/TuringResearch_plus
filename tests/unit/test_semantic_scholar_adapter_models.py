from __future__ import annotations

from turing_research.cache.keys import is_sha256_key
from turing_research_plus.adapters.cache import build_adapter_cache_key
from turing_research_plus.adapters.models import (
    SemanticScholarAuthorLookup,
    SemanticScholarPaperBatchLookup,
    SemanticScholarPaperIdLookup,
    SemanticScholarPaperListLookup,
    SemanticScholarPaperLookup,
    SemanticScholarRecommendationLookup,
)


def test_semantic_scholar_lookup_models_keep_live_disabled() -> None:
    requests = [
        SemanticScholarPaperLookup(query="VGGT"),
        SemanticScholarPaperIdLookup(paper_id="S2-1"),
        SemanticScholarPaperBatchLookup(paper_ids=["S2-1", "S2-2"]),
        SemanticScholarPaperListLookup(paper_id="S2-1"),
        SemanticScholarRecommendationLookup(paper_ids=["S2-1"]),
        SemanticScholarAuthorLookup(author_id="A1"),
    ]

    for request in requests:
        assert request.context.api_key_env == "SEMANTIC_SCHOLAR_API_KEY"
        assert request.context.live_enabled is False
        assert request.context.default_enabled is False
        assert request.context.fake_adapter_name == "FakeSemanticScholarAdapter"


def test_semantic_scholar_cache_key_is_sha256() -> None:
    request = SemanticScholarPaperLookup(query="VGGT", limit=3)

    key = build_adapter_cache_key(
        request.context.cache,
        request.query,
        request.model_dump(mode="json"),
    )

    assert is_sha256_key(str(key))
    assert "VGGT" not in str(key)
