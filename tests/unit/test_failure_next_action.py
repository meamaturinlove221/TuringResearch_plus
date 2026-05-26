from turing_research_plus.failure.models import FailureCategory
from turing_research_plus.failure.next_action import next_actions_for_category


def test_next_actions_for_missing_assets() -> None:
    actions = next_actions_for_category(FailureCategory.MISSING_ASSETS)

    assert any("adjacent predictions" in action for action in actions)
