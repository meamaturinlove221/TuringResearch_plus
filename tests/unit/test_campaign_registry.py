import pytest

from tuling_research_plus.budget.models import BudgetGate, BudgetLimit, BudgetUnit
from tuling_research_plus.campaign.models import CampaignSpec
from tuling_research_plus.campaign.registry import CampaignRegistry
from tuling_research_plus.ledger.models import StateLedger


def campaign_spec(campaign_id: str = "campaign-1") -> CampaignSpec:
    return CampaignSpec(
        campaign_id=campaign_id,
        title="Registered Campaign",
        budget_gate=BudgetGate(
            gate_id="budget-1",
            limits=[BudgetLimit(unit=BudgetUnit.REQUESTS, limit=1)],
        ),
        state_ledger=StateLedger(ledger_id="ledger-1", lane="lane-06"),
    )


def test_campaign_registry_register_get_and_list() -> None:
    registry = CampaignRegistry()
    spec = campaign_spec()

    registry.register(spec)

    assert registry.get("campaign-1") == spec
    assert registry.list() == [spec]


def test_campaign_registry_rejects_duplicate_campaign_id() -> None:
    registry = CampaignRegistry()
    registry.register(campaign_spec())

    with pytest.raises(ValueError):
        registry.register(campaign_spec())


def test_campaign_registry_reports_missing_campaign() -> None:
    registry = CampaignRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")
