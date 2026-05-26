from __future__ import annotations

from turing_research_plus.campaigns.preconditions import (
    evaluate_campaign_preconditions,
    render_campaign_precondition_report,
)


def test_preconditions_report_missing_inputs_without_fabrication() -> None:
    report = evaluate_campaign_preconditions("public_release", provided_inputs=[])

    assert report.ready_for_planning is False
    assert "passing tests" in report.missing_preconditions
    assert report.does_not_fabricate_missing_inputs is True
    assert report.requires_human_review is True


def test_preconditions_accept_campaign_aliases() -> None:
    report = evaluate_campaign_preconditions(
        "experiment_execution",
        provided_inputs=[
            "north star",
            "setup placeholder",
            "hard gates",
        ],
    )

    assert report.campaign_id == "experiment_planning"
    assert report.ready_for_planning is True
    assert report.missing_preconditions == []


def test_render_precondition_report_is_deterministic() -> None:
    report = evaluate_campaign_preconditions("hypothesis", provided_inputs=["north star"])
    rendered = render_campaign_precondition_report(report)

    assert "# Campaign Preconditions: hypothesis_formation" in rendered
    assert "Does not fabricate missing inputs: `true`" in rendered
