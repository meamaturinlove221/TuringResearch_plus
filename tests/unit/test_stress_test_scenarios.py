from __future__ import annotations

from turing_research_plus.stress_test.models import StressScenarioId
from turing_research_plus.stress_test.scenarios import (
    get_stress_scenario,
    list_stress_scenarios,
)


def test_stress_scenario_catalog_contains_required_scenarios() -> None:
    scenario_ids = {scenario.scenario_id for scenario in list_stress_scenarios()}

    assert scenario_ids == set(StressScenarioId)
    assert len(scenario_ids) == 9


def test_get_stress_scenario_returns_definition() -> None:
    scenario = get_stress_scenario(StressScenarioId.PRIVACY_LEAK)

    assert scenario.scenario_id == StressScenarioId.PRIVACY_LEAK
    assert "private" in scenario.purpose.lower()
    assert scenario.recommended_action
