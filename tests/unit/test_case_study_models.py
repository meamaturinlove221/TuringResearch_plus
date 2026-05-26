from __future__ import annotations

import pytest

from turing_research_plus.case_study.models import (
    CaseStudyClaimSafetyReport,
    CaseStudyDraft,
    CaseStudyRedactionReport,
    CaseStudySection,
)


def _section(section_id: str) -> CaseStudySection:
    return CaseStudySection(
        section_id=section_id,
        title=section_id.replace("-", " ").title(),
        bullets=["review-only bullet"],
        evidence_refs=["examples/vggt-human-prior-survey/research_knowledge_pack"],
    )


def test_case_study_draft_serializes_review_boundary() -> None:
    draft = CaseStudyDraft(
        case_study_id="demo",
        title="Demo",
        problem_background=_section("problem-background"),
        why_turingresearch_was_useful=_section("why-useful"),
        route_changes=_section("route-changes"),
        evidence_management=_section("evidence-management"),
        failures_and_blockers=_section("failures-and-blockers"),
        advisor_pack=_section("advisor-pack"),
        what_remains_human_work=_section("human-work"),
        what_not_to_claim=_section("what-not-to-claim"),
        redaction_report=CaseStudyRedactionReport(),
        claim_safety_report=CaseStudyClaimSafetyReport(),
    )

    payload = draft.model_dump(mode="json")

    assert payload["published"] is False
    assert payload["public_demo_only"] is True
    assert payload["requires_human_review"] is True
    assert len(draft.sections) == 8


def test_case_study_draft_cannot_publish() -> None:
    with pytest.raises(ValueError, match="must not publish"):
        CaseStudyDraft(
            case_study_id="bad",
            title="Bad",
            problem_background=_section("problem-background"),
            why_turingresearch_was_useful=_section("why-useful"),
            route_changes=_section("route-changes"),
            evidence_management=_section("evidence-management"),
            failures_and_blockers=_section("failures-and-blockers"),
            advisor_pack=_section("advisor-pack"),
            what_remains_human_work=_section("human-work"),
            what_not_to_claim=_section("what-not-to-claim"),
            redaction_report=CaseStudyRedactionReport(),
            claim_safety_report=CaseStudyClaimSafetyReport(),
            published=True,
        )
