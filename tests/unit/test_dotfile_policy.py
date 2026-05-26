from __future__ import annotations

from turing_research_plus.session_runtime.dotfile_policy import (
    evaluate_dotfile_policy,
)


def test_dotfile_policy_blocks_sensitive_dotfiles() -> None:
    decision = evaluate_dotfile_policy(".env")

    assert decision.release_blocker is True
    assert "dotfile-denylist" in decision.reasons


def test_dotfile_policy_allows_explicit_allowlist() -> None:
    decision = evaluate_dotfile_policy(".keep")

    assert decision.allowed is True
    assert decision.reasons == []


def test_dotfile_policy_blocks_unknown_dotfile() -> None:
    decision = evaluate_dotfile_policy(".python-version")

    assert decision.release_blocker is True
    assert "dotfile-not-allowlisted" in decision.reasons


def test_dotfile_policy_checks_nested_parts() -> None:
    decision = evaluate_dotfile_policy("notes/.ssh/config")

    assert "dotfile-denylist" in decision.reasons
    assert ".ssh" in decision.dotfile_parts
