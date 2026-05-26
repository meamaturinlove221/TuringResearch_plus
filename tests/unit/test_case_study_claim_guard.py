from __future__ import annotations

from turing_research_plus.case_study.claim_guard import guard_case_study_claims


def test_case_study_claim_guard_blocks_sparseconv_success() -> None:
    report = guard_case_study_claims("SparseConv3D route was successful in the experiment.")

    assert report.safe_to_publish is False
    assert report.findings
    assert "not established" in report.findings[0].reason
    assert "not-enough-evidence" in report.findings[0].replacement


def test_case_study_claim_guard_allows_conservative_wording() -> None:
    report = guard_case_study_claims(
        "SparseConv3D remains planned / not-enough-evidence."
    )

    assert report.safe_to_publish is True
    assert report.findings == []
