from __future__ import annotations

import pytest

from turing_research_plus.related_work.models import (
    PositioningClaim,
    RelatedWorkPositioningReport,
)


def test_related_work_report_rejects_definitive_safe_claim() -> None:
    with pytest.raises(ValueError, match="safe claims cannot be definitive"):
        RelatedWorkPositioningReport(
            project_topic="VGGT",
            safe_claims=[
                PositioningClaim(
                    text="Definitive no collision.",
                    basis="fixture",
                    caveat="none",
                )
            ],
        )


def test_related_work_report_is_json_serializable() -> None:
    report = RelatedWorkPositioningReport(project_topic="VGGT")

    payload = report.model_dump(mode="json")

    assert payload["project_topic"] == "VGGT"
    assert payload["requires_human_review"] is True
