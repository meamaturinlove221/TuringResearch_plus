from turing_research_plus.artifacts.models import EvidenceRef
from turing_research_plus.failure.attribution import build_failure_attribution_report
from turing_research_plus.failure.models import FailureCategory, FailureInstance


def evidence() -> EvidenceRef:
    return EvidenceRef(source_id="ledger", locator="V260", quote="missing assets")


def test_attribution_uses_evidence_when_present() -> None:
    report = build_failure_attribution_report(
        FailureInstance(
            failure_id="f-v260",
            text="missing adjacent predictions",
            evidence_refs=[evidence()],
        )
    )

    assert report.category == FailureCategory.MISSING_ASSETS
    assert report.requires_human_review is False


def test_attribution_requires_human_review_without_evidence() -> None:
    report = build_failure_attribution_report(
        FailureInstance(failure_id="f-visual", text="missing board proof")
    )

    assert report.category == FailureCategory.VISUAL_PROOF_INSUFFICIENT
    assert report.requires_human_review is True
