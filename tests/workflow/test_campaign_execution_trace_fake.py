from __future__ import annotations

from pathlib import Path

from turing_research_plus.campaigns import (
    build_campaign_execution_trace,
    render_campaign_execution_trace,
)

ROOT = Path(__file__).resolve().parents[2]


def test_campaign_execution_trace_fake_workflow() -> None:
    trace = build_campaign_execution_trace(
        "stress test unsafe claim review",
        provided_inputs=["candidate claim or release surface"],
    )
    rendered = render_campaign_execution_trace(trace)

    assert trace.campaign_id == "stress_test"
    assert trace.fake_trace is True
    assert trace.ready_for_execution is False
    assert all(step.executed is False for step in trace.steps)
    assert "proposed outputs are not observed evidence" in rendered
    assert "master orchestrator remains in control" in rendered


def test_campaign_execution_trace_docs_and_fixture_are_public_safe() -> None:
    paths = [
        ROOT / "docs" / "campaign-execution-trace.md",
        ROOT / "examples" / "campaigns" / "execution_trace_demo" / "README.md",
        ROOT / "examples" / "campaigns" / "execution_trace_demo" / "trace.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    assert "fake execution trace" in combined
    assert "not an agent runtime" in combined
    assert "does not execute tools" in combined
    assert "does not call an LLM" in combined
    assert "does not use network" in combined
    assert "does not mutate Evidence Ledger" in combined
    assert "Tuling" + "Research" not in combined
    assert "D:" + "/vggt" not in combined
    assert "observed result" not in combined.lower()
