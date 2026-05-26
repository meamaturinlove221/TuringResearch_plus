from __future__ import annotations

from turing_research_plus.object_store.models import ObjectArtifactStatus
from turing_research_plus.object_store.safety import (
    omitted_reason_for_object,
    safety_warnings_for_object_key,
    status_for_object_warnings,
)


def test_object_store_safety_marks_large_npz_metadata_only() -> None:
    warnings = safety_warnings_for_object_key(
        "modal-sparseconv-review/large/predictions.npz",
        size=250_000_000,
    )

    assert "summary-only-required" in warnings
    assert "file-too-large" in warnings
    assert status_for_object_warnings(warnings) == ObjectArtifactStatus.LARGE_METADATA_ONLY
    assert "metadata-only" in omitted_reason_for_object(warnings)


def test_object_store_safety_marks_smplx_model_unsafe() -> None:
    warnings = safety_warnings_for_object_key(
        "modal-sparseconv-review/private/SMPLX_model.pkl",
        size=100_000_000,
    )

    assert "forbidden-secret-or-body-model-pattern" in warnings
    assert status_for_object_warnings(warnings) == ObjectArtifactStatus.UNSAFE
