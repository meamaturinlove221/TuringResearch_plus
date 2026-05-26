from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import semantic_scholar_live_skip_reason
from turing_research_plus.adapters.models import SemanticScholarPaperLookup
from turing_research_plus.adapters.semantic_scholar import SemanticScholarLiveAdapter


@pytest.mark.live
def test_semantic_scholar_live_lookup_optional() -> None:
    reason = semantic_scholar_live_skip_reason()
    if reason is not None:
        pytest.skip(reason)

    request = SemanticScholarPaperLookup(query="VGGT", limit=1)
    request.context.dry_run = False
    request.context.live_enabled = True

    result = SemanticScholarLiveAdapter().paper_lookup(request)

    assert result.status == "ok"
    assert result.source_metadata
    assert result.source_metadata[0].provider == "semantic_scholar"
    assert result.source_metadata[0].human_verified is False
