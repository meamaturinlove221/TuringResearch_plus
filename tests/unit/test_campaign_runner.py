import pytest
from pydantic import ValidationError

from turing_research_plus.budget.models import BudgetGate, BudgetLimit, BudgetUnit
from turing_research_plus.campaign.models import (
    CampaignMode,
    CampaignSpec,
    QualityGateSpec,
    SOPExecutionMode,
    SOPSpec,
    StrategySpec,
    TacticSpec,
    WorkflowStatus,
)
from turing_research_plus.campaign.runner import CampaignRunner
from turing_research_plus.ledger.models import LedgerEventType, StateLedger
from turing_research_plus.subtask.models import TaskProfile


def budget_gate(
    current: float = 1,
    target: float = 1,
    minimum_ratio: float = 1,
    deviation_reason: str | None = None,
) -> BudgetGate:
    return BudgetGate(
        gate_id="budget-1",
        target=target,
        current=current,
        minimum_ratio=minimum_ratio,
        deviation_reason=deviation_reason,
        limits=[BudgetLimit(unit=BudgetUnit.REQUESTS, limit=10)],
    )


def fake_campaign(gate: BudgetGate | None = None) -> CampaignSpec:
    return CampaignSpec(
        campaign_id="campaign-1",
        title="Fake Campaign",
        mode=CampaignMode.FAKE_SERVICE,
        budget_gate=gate or budget_gate(),
        state_ledger=StateLedger(ledger_id="ledger-1", lane="lane-06"),
        strategies=[
            StrategySpec(
                strategy_id="strategy-1",
                title="Strategy",
                tactics=[
                    TacticSpec(
                        tactic_id="tactic-1",
                        title="Tactic",
                        sops=[
                            SOPSpec(
                                sop_id="sop-1",
                                title="Direct SOP",
                                execution_mode=SOPExecutionMode.DIRECT,
                            ),
                            SOPSpec(
                                sop_id="sop-2",
                                title="Subtask SOP",
                                execution_mode=SOPExecutionMode.SUBTASK,
                            ),
                        ],
                    )
                ],
            )
        ],
        quality_gates=[
            QualityGateSpec(gate_id="has-artifact", description="At least one artifact")
        ],
    )


def test_fake_campaign_runs_end_to_end_and_triggers_checkpoint() -> None:
    checkpoints = []
    runner = CampaignRunner(checkpoint_hook=lambda run: checkpoints.append(run.run_id))

    result = runner.run(fake_campaign())

    assert result.status == WorkflowStatus.COMPLETED
    assert result.selected_strategy_id == "strategy-1"
    assert len(result.artifacts) == 2
    assert result.quality_gate_results == {"has-artifact": True}
    assert checkpoints == [result.run_id]


def test_budget_gate_blocks_early_completion() -> None:
    result = CampaignRunner().run(
        fake_campaign(budget_gate(current=1, target=10, minimum_ratio=0.5))
    )

    assert result.status == WorkflowStatus.BLOCKED
    assert result.blocked_reason == "BudgetGate minimum ratio not met"
    assert result.artifacts == []
    assert result.ledger.blockers[0].event_type == LedgerEventType.BLOCKED


def test_deviation_reason_allows_controlled_completion() -> None:
    result = CampaignRunner().run(
        fake_campaign(
            budget_gate(
                current=1,
                target=10,
                minimum_ratio=0.5,
                deviation_reason="Fixture intentionally runs below budget floor.",
            )
        )
    )

    assert result.status == WorkflowStatus.COMPLETED
    assert len(result.artifacts) == 2
    assert any("Budget deviation accepted" in event.message for event in result.ledger.events)


def test_state_ledger_records_artifacts() -> None:
    result = CampaignRunner().run(fake_campaign())

    assert len(result.ledger.artifacts) == 2
    assert any(event.event_type == LedgerEventType.ARTIFACT for event in result.ledger.events)


def test_campaign_result_serializes_to_markdown() -> None:
    result = CampaignRunner().run(fake_campaign())

    markdown = result.to_markdown()

    assert "# Campaign Result: campaign-1" in markdown
    assert "- Status: `completed`" in markdown
    assert "## Quality Gates" in markdown
    assert "## Artifacts" in markdown


def test_task_profile_validates_non_dry_run_tools() -> None:
    with pytest.raises(ValidationError):
        TaskProfile(
            name="profile-1",
            role="worker",
            goal="Execute non dry-run work.",
            input_schema={"type": "object"},
            output_schema={"type": "object"},
            dry_run=False,
        )
