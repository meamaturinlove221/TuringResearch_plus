from __future__ import annotations

import pytest
from pydantic import ValidationError

from turing_research_plus.handoff.models import (
    HandoffBundleManifest,
    HandoffBundleType,
    HandoffFileRecord,
    HandoffStatusLabel,
)


def test_handoff_manifest_requires_manual_review() -> None:
    manifest = HandoffBundleManifest(
        bundle_id="fixture",
        source_machine_label="main",
        bundle_type=HandoffBundleType.VGGT_DOGFOOD,
        status_labels=[HandoffStatusLabel.REQUIRES_HUMAN_REVIEW],
    )

    assert manifest.project_name == "TuringResearch Plus"
    assert manifest.manual_review_required is True


def test_handoff_manifest_rejects_non_review_bundle() -> None:
    with pytest.raises(ValidationError):
        HandoffBundleManifest(
            bundle_id="fixture",
            source_machine_label="main",
            bundle_type=HandoffBundleType.MANUAL,
            manual_review_required=False,
        )


def test_omitted_file_requires_reason() -> None:
    with pytest.raises(ValidationError):
        HandoffFileRecord(relative_path="secret.env", included=False)
