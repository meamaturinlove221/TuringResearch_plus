from __future__ import annotations

import pytest

from turing_research_plus.paper_digest.models import (
    PaperDigest,
    PaperDigestInput,
    PaperDigestSourceStatus,
)


def test_paper_digest_serializes_review_boundary() -> None:
    digest = PaperDigest(
        paper_id="paper-1",
        title="Paper Fixture",
        source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
        pass1_summary="review scaffold only",
        method_contribution="requires-real-paper-review",
        requires_real_paper=True,
    )

    payload = digest.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["requires_real_paper"] is True
    assert payload["human_verified"] is False


def test_paper_digest_rejects_complete_review_claim() -> None:
    with pytest.raises(ValueError, match="complete paper review"):
        PaperDigest(
            paper_id="paper-1",
            title="Paper Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            pass1_summary="complete paper review",
            method_contribution="requires-real-paper-review",
        )


def test_paper_digest_input_rejects_fake_verified_source() -> None:
    with pytest.raises(ValueError, match="cannot be human verified"):
        PaperDigestInput(
            paper_id="paper-1",
            title="Paper Fixture",
            source_status=PaperDigestSourceStatus.FAKE_OR_MANUAL_NOTE,
            source_text="# fixture",
            human_verified=True,
        )
