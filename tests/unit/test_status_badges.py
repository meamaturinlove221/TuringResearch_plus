from __future__ import annotations

from pathlib import Path

from turing_research_plus.dashboard.models import DashboardBadge
from turing_research_plus.dashboard.status_badges import badge_label, badges_for_run
from turing_research_plus.run_ingest.modal_ingestor import ingest_modal_run
from turing_research_plus.run_ingest.models import RunIngestRequest, RunSourceType

FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "vggt-human-prior-survey"
    / "run_ingest_fixtures"
    / "modal_run_fixture"
)


def test_status_badges_for_modal_fixture() -> None:
    report = ingest_modal_run(
        RunIngestRequest(source_type=RunSourceType.MODAL_FIXTURE, source_path=FIXTURE)
    )

    badges = badges_for_run(report)

    assert DashboardBadge.ROUTE_EXHAUSTED in badges
    assert DashboardBadge.NOT_ENOUGH_EVIDENCE in badges
    assert DashboardBadge.REQUIRES_HUMAN_REVIEW in badges
    assert badge_label(DashboardBadge.ROUTE_EXHAUSTED) == "[ROUTE_EXHAUSTED]"
