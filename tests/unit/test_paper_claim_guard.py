from __future__ import annotations

import pytest

from turing_research_plus.paper_write.claim_guard import (
    PaperClaimGuardReport,
    evaluate_paper_claims,
    render_paper_claim_guard_report,
)


def test_paper_claim_guard_blocks_known_unsafe_claims_when_marked_blocked() -> None:
    report = evaluate_paper_claims(
        {
            "results": "Do not claim SparseConv3D success without backend evidence.",
            "paper": "This is not final paper text.",
        }
    )

    assert report.risky_unblocked_claims == []
    assert any("SparseConv3D success" in claim for claim in report.blocked_claims)
    assert report.final_paper_claim_blocked is True
    assert report.fake_observed_claim_blocked is True


def test_paper_claim_guard_detects_unblocked_risky_claims() -> None:
    report = evaluate_paper_claims({"results": "SparseConv3D success improves results."})

    assert report.risky_unblocked_claims


def test_paper_claim_guard_requires_boundaries() -> None:
    with pytest.raises(ValueError):
        PaperClaimGuardReport(final_paper_claim_blocked=False)

    rendered = render_paper_claim_guard_report(evaluate_paper_claims({}))
    assert "This beta package does not write final paper claims." in rendered
