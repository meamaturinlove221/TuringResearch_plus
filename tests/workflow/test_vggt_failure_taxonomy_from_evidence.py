from turing_research_plus.failure.attribution import build_failure_attribution_report
from turing_research_plus.failure.models import FailureCategory, FailureInstance


def test_vggt_failure_taxonomy_expected_rules() -> None:
    cases = {
        "V260 missing adjacent predictions / semantic assets": FailureCategory.MISSING_ASSETS,
        "SparseConv3D backend unavailable": FailureCategory.SPARSE_BACKEND_UNAVAILABLE,
        "missing board proof": FailureCategory.VISUAL_PROOF_INSUFFICIENT,
        "V129 hairline degradation": FailureCategory.HAIRLINE_REGRESSION,
        "fallback-only path": FailureCategory.FALLBACK_ONLY,
        "report-only output": FailureCategory.REPORT_ONLY,
        "no real experiment evidence": FailureCategory.NOT_ENOUGH_EVIDENCE,
    }

    for text, category in cases.items():
        report = build_failure_attribution_report(
            FailureInstance(failure_id=f"case-{category.value}", text=text)
        )
        assert report.category == category
        assert report.requires_human_review is True
        assert report.next_actions
