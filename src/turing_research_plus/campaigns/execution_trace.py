"""Fake campaign execution trace generation.

The trace records the shape of a campaign run without executing skills, tools,
LLM calls, network calls, or evidence updates.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.campaigns.execution_plan import (
    CampaignExecutionPlan,
    build_campaign_execution_plan,
)


class CampaignTraceStep(BaseModel):
    """One review-only trace step."""

    model_config = ConfigDict(extra="forbid")

    step_id: str = Field(pattern=r"^[a-z0-9_]+$")
    label: str = Field(min_length=1)
    status: str = Field(pattern=r"^(not_executed|blocked_missing_preconditions)$")
    description: str = Field(min_length=1)
    inputs: list[str] = Field(default_factory=list)
    expected_outputs: list[str] = Field(default_factory=list)
    safety_notes: list[str] = Field(min_length=1)
    executed: bool = False
    called_tool: bool = False
    called_llm: bool = False
    used_network: bool = False
    wrote_evidence_ledger: bool = False
    evidence_status: str = "proposed-only"


class CampaignExecutionTrace(BaseModel):
    """Fake trace for a campaign plan.

    A trace is an audit artifact. It is not an agent runtime and does not run
    campaign skills.
    """

    model_config = ConfigDict(extra="forbid")

    trace_id: str = Field(pattern=r"^campaign-trace-[a-z0-9_-]+$")
    task_description: str = Field(min_length=1)
    campaign_id: str = Field(min_length=1)
    recommended_skill: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    confidence: float = Field(ge=0, le=1)
    provided_inputs: list[str] = Field(default_factory=list)
    missing_preconditions: list[str] = Field(default_factory=list)
    steps: list[CampaignTraceStep] = Field(min_length=1)
    proposed_outputs: list[str] = Field(min_length=1)
    safety_notes: list[str] = Field(min_length=1)
    fake_trace: bool = True
    does_not_execute: bool = True
    does_not_call_llm: bool = True
    does_not_use_network: bool = True
    does_not_mutate_evidence_ledger: bool = True
    replaces_master_orchestrator: bool = False
    requires_human_review: bool = True

    @property
    def ready_for_execution(self) -> bool:
        """Return False because this is not an execution runtime."""

        return False

    @property
    def blocked(self) -> bool:
        """Return whether the trace has missing preconditions."""

        return bool(self.missing_preconditions)


def build_campaign_execution_trace(
    task_description: str,
    *,
    provided_inputs: list[str] | None = None,
) -> CampaignExecutionTrace:
    """Build a deterministic fake trace from a review-only campaign plan."""

    plan = build_campaign_execution_plan(
        task_description,
        provided_inputs=provided_inputs,
    )
    status = (
        "not_executed"
        if plan.precondition_report.ready_for_planning
        else "blocked_missing_preconditions"
    )
    return CampaignExecutionTrace(
        trace_id=_trace_id(plan),
        task_description=plan.task_description,
        campaign_id=plan.campaign_id,
        recommended_skill=plan.recommended_skill,
        confidence=plan.confidence,
        provided_inputs=plan.precondition_report.provided_inputs,
        missing_preconditions=plan.precondition_report.missing_preconditions,
        steps=[
            _step(
                "route_campaign",
                "Route campaign",
                "not_executed",
                "Record the campaign routing decision without running the skill.",
                inputs=[plan.task_description],
                expected_outputs=["campaign recommendation", "skill handoff"],
                safety_notes=["routing is advisory only"],
            ),
            _step(
                "check_preconditions",
                "Check preconditions",
                status,
                "Record provided and missing preconditions without fabricating inputs.",
                inputs=plan.precondition_report.provided_inputs,
                expected_outputs=["precondition report"],
                safety_notes=["missing inputs stay visible"],
            ),
            _step(
                "prepare_handoff",
                "Prepare skill handoff",
                status,
                "Prepare a manual handoff for the recommended skill.",
                inputs=[plan.recommended_skill],
                expected_outputs=["manual skill handoff"],
                safety_notes=["does not execute the skill"],
            ),
            _step(
                "record_proposed_outputs",
                "Record proposed outputs",
                status,
                "List expected outputs for human review.",
                inputs=plan.expected_outputs,
                expected_outputs=plan.expected_outputs,
                safety_notes=["proposed outputs are not observed evidence"],
            ),
            _step(
                "human_review_gate",
                "Human review gate",
                "not_executed",
                "Require human review before any implementation or public claim.",
                inputs=plan.next_steps,
                expected_outputs=["review decision", "next manual action"],
                safety_notes=["master orchestrator remains in control"],
            ),
        ],
        proposed_outputs=plan.expected_outputs,
        safety_notes=[
            *plan.safety_notes,
            "does not execute tools",
            "does not mutate evidence ledger",
            "fake trace is not observed evidence",
        ],
    )


def trace_from_plan(plan: CampaignExecutionPlan) -> CampaignExecutionTrace:
    """Build a fake trace from an existing plan."""

    return build_campaign_execution_trace(
        plan.task_description,
        provided_inputs=plan.precondition_report.provided_inputs,
    )


def _step(
    step_id: str,
    label: str,
    status: str,
    description: str,
    *,
    inputs: list[str],
    expected_outputs: list[str],
    safety_notes: list[str],
) -> CampaignTraceStep:
    return CampaignTraceStep(
        step_id=step_id,
        label=label,
        status=status,
        description=description,
        inputs=inputs,
        expected_outputs=expected_outputs,
        safety_notes=safety_notes,
    )


def _trace_id(plan: CampaignExecutionPlan) -> str:
    normalized = plan.campaign_id.replace("_", "-")
    return f"campaign-trace-{normalized}"
