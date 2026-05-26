from __future__ import annotations

from turing_research_plus.git_handoff.memory_policy import (
    render_memory_policy,
    validate_memory_text,
)


def test_memory_policy_flags_secret_like_content() -> None:
    warnings = validate_memory_text("OPENAI_API_KEY=sk-not-real-but-secretlike")

    assert "possible-secret-value" in warnings


def test_memory_policy_flags_memory_as_only_truth() -> None:
    warnings = validate_memory_text("MEMORY is the only source of truth.")

    assert "memory-cannot-be-only-source-of-truth" in warnings


def test_render_memory_policy_states_source_of_truth() -> None:
    text = render_memory_policy()

    assert "Evidence Ledger" in text
    assert "not the only source of truth" in text
