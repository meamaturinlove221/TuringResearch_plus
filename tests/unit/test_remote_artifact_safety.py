from __future__ import annotations

from turing_research_plus.remote_artifacts.models import RemoteArtifactStatus
from turing_research_plus.remote_artifacts.safety import (
    duplicate_key,
    stable_artifact_id,
    unified_status_from_warnings,
)


def test_unified_status_prioritizes_unsafe_over_metadata_only() -> None:
    assert (
        unified_status_from_warnings(
            ["summary-only-required", "forbidden-secret-or-body-model-pattern"]
        )
        == RemoteArtifactStatus.UNSAFE
    )
    assert unified_status_from_warnings(["file-too-large"]) == RemoteArtifactStatus.METADATA_ONLY
    assert unified_status_from_warnings([]) == RemoteArtifactStatus.SELECTED


def test_stable_artifact_id_and_duplicate_key() -> None:
    assert (
        stable_artifact_id("github:repo:main", "review/final_status.json")
        == "github:repo:main:review__final_status.json"
    )
    assert duplicate_key("a/b/final_status.json", None) == "path:final_status.json"
    assert duplicate_key("a/b/final_status.json", "a" * 64) == f"sha256:{'a' * 64}"
