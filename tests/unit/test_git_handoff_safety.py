from __future__ import annotations

from pathlib import Path

from turing_research_plus.git_handoff.safety import (
    safety_warnings_for_path,
    safety_warnings_for_text,
)


def test_safety_flags_env_and_api_keys() -> None:
    warnings = safety_warnings_for_text("SEMANTIC_SCHOLAR_API_KEY=secretvalue123")

    assert "possible-secret-value" in warnings


def test_safety_flags_body_model_paths() -> None:
    assert "forbidden-body-model-like-name" in safety_warnings_for_path(
        Path("models") / "SMPLX_NEUTRAL.npz"
    )
    assert "forbidden-private-or-secret-path" in safety_warnings_for_path(
        Path("private_data") / "summary.md"
    )
