from __future__ import annotations

from pathlib import Path

from turing_research_plus.handoff.safety import (
    omitted_reason,
    safety_warnings_for_path,
    should_include_file,
)


def test_env_files_are_forbidden() -> None:
    warnings = safety_warnings_for_path(Path(".env"))

    assert "forbidden-env-file" in warnings
    assert should_include_file(Path(".env")) is False


def test_body_model_and_npz_are_summary_only() -> None:
    warnings = safety_warnings_for_path(Path("models") / "SMPLX_NEUTRAL.npz")

    assert "summary-only-required" in warnings
    assert "forbidden-secret-or-body-model-pattern" in warnings
    assert "summary-only" in omitted_reason(Path("x.npz"), warnings)


def test_large_file_is_omitted() -> None:
    warnings = safety_warnings_for_path(Path("summary.json"), file_size=10, max_size=3)

    assert warnings == ["file-too-large"]


def test_markdown_summary_is_allowed() -> None:
    assert should_include_file(Path("reports") / "summary.md", file_size=128) is True
