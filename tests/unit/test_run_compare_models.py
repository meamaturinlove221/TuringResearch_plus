from __future__ import annotations

import pytest

from turing_research_plus.run_compare.models import (
    ArtifactCompletenessEntry,
    RunComparisonInput,
    RunComparisonReport,
)


def test_run_comparison_report_serializes() -> None:
    report = RunComparisonReport(
        compared_runs=["V999"],
        artifact_completeness=[
            ArtifactCompletenessEntry(
                run_id="V999",
                present_count=1,
                missing_count=1,
                missing_artifacts=["predictions.npz"],
            )
        ],
        unsupported_claims=["SparseConv3D success requires real backend evidence."],
        next_actions=["V999: collect real sparse backend evidence."],
    )

    payload = report.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["image_understanding_performed"] is False


def test_run_comparison_report_cannot_claim_image_understanding() -> None:
    with pytest.raises(ValueError, match="must not claim image understanding"):
        RunComparisonReport(
            compared_runs=["V129"],
            image_understanding_performed=True,
        )


def test_run_comparison_input_requires_review() -> None:
    with pytest.raises(ValueError, match="require human review"):
        RunComparisonInput(run_id="V770", requires_human_review=False)
