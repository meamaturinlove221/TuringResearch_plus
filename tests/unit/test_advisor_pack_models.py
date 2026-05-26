import pytest

from turing_research_plus.advisor.models import AdvisorPack, AdvisorReadinessStatus


def test_advisor_pack_requires_not_ready_claims_when_blocked() -> None:
    with pytest.raises(ValueError, match="not_ready_claims"):
        AdvisorPack(
            pack_id="pack",
            advisor_goal="Summarize status.",
            current_route_summary="Route summary.",
            what_changed_since_last_update=["Changed route."],
            observed_evidence=[],
            limitations=[],
            blockers=[],
            visual_readiness=AdvisorReadinessStatus.BLOCKED,
            not_ready_claims=[],
            next_actions=["Collect evidence."],
            suggested_advisor_message="Message.",
            required_human_review=[],
        )


def test_advisor_pack_serializes_markdown() -> None:
    pack = AdvisorPack(
        pack_id="pack",
        advisor_goal="Summarize status.",
        current_route_summary="Route summary.",
        what_changed_since_last_update=["Changed route."],
        observed_evidence=["V770 local-observed."],
        limitations=["Visual evidence missing."],
        blockers=["No board inventory."],
        visual_readiness=AdvisorReadinessStatus.BLOCKED,
        not_ready_claims=["No advisor-ready visual proof."],
        next_actions=["Collect visual inventory."],
        suggested_advisor_message="Short message.",
        required_human_review=["Visual evidence review."],
    )

    markdown = pack.to_markdown()

    assert "# Advisor Summary" in markdown
    assert "No advisor-ready visual proof" in markdown
    assert "Visual evidence review" in markdown
