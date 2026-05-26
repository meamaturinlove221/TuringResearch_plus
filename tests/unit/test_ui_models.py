from __future__ import annotations

import pytest

from turing_research_plus.ui.models import (
    DashboardSection,
    DashboardSectionKind,
    StaticDashboardSpec,
)


def test_static_dashboard_spec_serializes() -> None:
    spec = StaticDashboardSpec(
        dashboard_id="dash-1",
        title="Dashboard",
        project_name="Project",
        output_dir="out",
        sections=[
            DashboardSection(
                kind=DashboardSectionKind.PROJECT_OVERVIEW,
                title="Overview",
                markdown="Review only.",
            )
        ],
    )

    payload = spec.model_dump(mode="json")

    assert payload["requires_human_review"] is True
    assert payload["ui_executed_experiment"] is False
    assert payload["server_required"] is False


def test_static_dashboard_spec_rejects_execution_claim() -> None:
    with pytest.raises(ValueError, match="must not claim experiment execution"):
        StaticDashboardSpec(
            dashboard_id="dash-1",
            title="Dashboard",
            project_name="Project",
            output_dir="out",
            sections=[
                DashboardSection(
                    kind=DashboardSectionKind.PROJECT_OVERVIEW,
                    title="Overview",
                    markdown="Review only.",
                )
            ],
            ui_executed_experiment=True,
        )
