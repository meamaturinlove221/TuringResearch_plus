from turing_research_plus.budget.models import BudgetGate, BudgetLimit, BudgetUnit
from turing_research_plus.campaign.models import CampaignMode, CampaignSpec
from turing_research_plus.ledger.models import StateLedger


def test_campaign_defaults_to_dry_run_mode() -> None:
    campaign = CampaignSpec(
        campaign_id="campaign-1",
        title="Skeleton campaign",
        budget_gate=BudgetGate(
            gate_id="budget-1",
            limits=[BudgetLimit(unit=BudgetUnit.SECONDS, limit=30)],
        ),
        state_ledger=StateLedger(ledger_id="ledger-1", lane="lane-06"),
    )

    assert campaign.mode == CampaignMode.DRY_RUN
    assert campaign.dry_run is True
    assert campaign.fake_service is False
