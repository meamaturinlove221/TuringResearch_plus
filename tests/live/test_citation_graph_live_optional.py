from __future__ import annotations

import pytest

from turing_research_plus.adapters.live_test_markers import semantic_scholar_live_skip_reason
from turing_research_plus.adapters.semantic_scholar import SemanticScholarLiveAdapter
from turing_research_plus.citation_graph.expander import CitationGraphExpander
from turing_research_plus.citation_graph.models import (
    CitationGraphRequest,
    CitationGraphSourceAdapter,
)


@pytest.mark.live
def test_citation_graph_live_optional() -> None:
    reason = semantic_scholar_live_skip_reason()
    if reason is not None:
        pytest.skip(reason)

    request = CitationGraphRequest(
        graph_id="live-vggt-smoke",
        seed_topics=["VGGT"],
        expansion_depth=0,
        max_nodes=1,
        source_adapter=CitationGraphSourceAdapter.LIVE_SEMANTIC_SCHOLAR,
        live_enabled=True,
        dry_run=False,
    )

    graph = CitationGraphExpander(SemanticScholarLiveAdapter()).expand(request)

    assert graph.source_adapter == CitationGraphSourceAdapter.LIVE_SEMANTIC_SCHOLAR
    assert graph.requires_human_review is True
