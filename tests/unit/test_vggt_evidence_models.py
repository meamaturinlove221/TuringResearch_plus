import pytest

from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.vggt.evidence_models import (
    VGGTEvidenceLedger,
    VGGTEvidenceRow,
    VGGTEvidenceStatus,
)


def ref() -> EvidenceRef:
    return EvidenceRef(
        source_id="scan",
        locator="line",
        quote="Local scan summary records candidate roots.",
    )


def test_vggt_evidence_status_values() -> None:
    assert {status.value for status in VGGTEvidenceStatus} == {
        "observed",
        "local-observed",
        "planned",
        "fake-data",
        "failed",
        "hard-blocked",
        "requires-real-paper",
        "requires-real-experiment",
        "requires-human-review",
        "not-enough-evidence",
    }


def test_local_observed_requires_source_files() -> None:
    with pytest.raises(ValueError, match="source_files"):
        VGGTEvidenceRow(
            run_id="run",
            version_label="V770",
            claim="Local diagnostic exists.",
            status=VGGTEvidenceStatus.LOCAL_OBSERVED,
            evidence_refs=[ref()],
        )


def test_requires_human_review_requires_blocker_or_next_action() -> None:
    with pytest.raises(ValueError, match="blockers or next_actions"):
        VGGTEvidenceRow(
            run_id="run",
            version_label="V120",
            claim="Needs review.",
            status=VGGTEvidenceStatus.REQUIRES_HUMAN_REVIEW,
        )


def test_ledger_markdown_serialization_includes_missing_inputs() -> None:
    row = VGGTEvidenceRow(
        run_id="run",
        version_label="V900",
        claim="Entrypoint observed as engineering context.",
        status=VGGTEvidenceStatus.OBSERVED,
        evidence_refs=[ref()],
    )
    ledger = VGGTEvidenceLedger(
        ledger_id="ledger",
        run_id="run",
        rows=[row],
        missing_inputs=["missing.json"],
    )

    markdown = ledger.to_markdown()

    assert "V900" in markdown
    assert "`missing.json`" in markdown

