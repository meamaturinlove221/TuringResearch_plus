from __future__ import annotations

import pytest

from turing_research_plus.remote_artifacts.models import (
    ArtifactRef,
    RemoteArtifactSourceKind,
    RemoteArtifactStatus,
    UnifiedRemoteArtifactReport,
)


def test_remote_artifact_ref_cannot_be_verified() -> None:
    with pytest.raises(ValueError, match="indexed, not verified"):
        ArtifactRef(
            artifact_id="github:final_status",
            source_id="github:repo:main",
            source_kind=RemoteArtifactSourceKind.GITHUB,
            path="review/final_status.json",
            status=RemoteArtifactStatus.SELECTED,
            human_verified=True,
        )


def test_unified_remote_artifact_report_serializes_and_exports_markdown() -> None:
    artifact = ArtifactRef(
        artifact_id="github:final_status",
        source_id="github:repo:main",
        source_kind=RemoteArtifactSourceKind.GITHUB,
        path="review/final_status.json",
        size=512,
        status=RemoteArtifactStatus.SELECTED,
    )
    report = UnifiedRemoteArtifactReport(
        normalized_artifacts=[artifact],
        selected_artifacts=[artifact],
        proposed_imports=[{"path": artifact.path, "status": "requires-human-review"}],
    )

    payload = report.model_dump(mode="json")
    markdown = report.to_markdown()

    assert payload["requires_human_review"] is True
    assert payload["human_verified"] is False
    assert "review/final_status.json" in markdown
