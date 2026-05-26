from __future__ import annotations

import pytest

from turing_research_plus.dashboard_api.models import (
    DashboardDataBundle,
    DashboardEvidenceEntry,
    DashboardEvidenceSummary,
    DashboardProjectSummary,
)


def test_evidence_summary_rejects_observed_demo_status() -> None:
    with pytest.raises(ValueError, match="observed"):
        DashboardEvidenceSummary(
            ledger_id="demo",
            status="demo-only",
            entries=[
                DashboardEvidenceEntry(
                    evidence_id="e1",
                    status="observed",
                    claim="fake claim",
                    source_ref="demo.md",
                )
            ],
        )


def test_dashboard_bundle_requires_safety_flags() -> None:
    project = DashboardProjectSummary(
        project_id="demo",
        title="Demo",
        status="demo only",
        topic="topic",
        north_star="north star",
    )
    evidence = DashboardEvidenceSummary(ledger_id="ledger", status="demo-only")

    with pytest.raises(ValueError, match="safety boundary"):
        DashboardDataBundle(
            bundle_id="bad",
            project=project,
            evidence=evidence,
            artifacts={"records": []},
            paper={"title": "Paper"},
            no_raw_data=False,
        )
