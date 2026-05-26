from __future__ import annotations

from turing_research_plus.campaigns.execution_trace import build_campaign_execution_trace
from turing_research_plus.campaigns.trace_renderer import render_campaign_execution_trace


def test_render_campaign_execution_trace_mentions_non_runtime_boundary() -> None:
    trace = build_campaign_execution_trace(
        "Collect literature and web source context for a paper survey",
        provided_inputs=["source list", "source hygiene boundary"],
    )
    rendered = render_campaign_execution_trace(trace)

    assert "# Campaign Execution Trace: knowledge_acquisition" in rendered
    assert "Fake trace: `true`" in rendered
    assert "Ready for execution: `false`" in rendered
    assert "Does not execute: `true`" in rendered
    assert "Does not call LLM: `true`" in rendered
    assert "Does not use network: `true`" in rendered
    assert "Does not mutate Evidence Ledger: `true`" in rendered
    assert "`route_campaign`" in rendered
    assert "`human_review_gate`" in rendered
