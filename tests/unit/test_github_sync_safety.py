from __future__ import annotations

from turing_research_plus.github_sync.safety import (
    omitted_reason_for_artifact,
    safety_warnings_for_artifact_path,
    should_select_artifact,
)


def test_github_safety_blocks_secret_and_body_model_patterns() -> None:
    warnings = safety_warnings_for_artifact_path("private/SMPLX_model.pkl", size=100)

    assert "summary-only-required" in warnings
    assert "forbidden-secret-or-body-model-pattern" in warnings
    assert not should_select_artifact("private/SMPLX_model.pkl", size=100)
    assert "summary-only" in omitted_reason_for_artifact(warnings)


def test_github_safety_blocks_large_files() -> None:
    warnings = safety_warnings_for_artifact_path("review/predictions.txt", size=5_000_000)

    assert warnings == ["file-too-large"]
    assert omitted_reason_for_artifact(warnings) == "artifact exceeds max selected file size"


def test_github_safety_allows_small_review_markdown() -> None:
    assert should_select_artifact("review/failure_report.md", size=1024)
