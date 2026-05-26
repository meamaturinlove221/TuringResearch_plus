"""Review-only campaign execution plan recommendations."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from turing_research_plus.campaigns.preconditions import (
    CampaignPreconditionReport,
    evaluate_campaign_preconditions,
)
from turing_research_plus.campaigns.router import route_campaign


class CampaignExecutionPlan(BaseModel):
    """Recommended campaign plan that does not execute anything."""

    model_config = ConfigDict(extra="forbid")

    task_description: str = Field(min_length=1)
    campaign_id: str = Field(min_length=1)
    recommended_skill: str = Field(pattern=r"^turingresearch-[a-z0-9-]+$")
    confidence: float = Field(ge=0, le=1)
    precondition_report: CampaignPreconditionReport
    expected_outputs: list[str] = Field(min_length=1)
    safety_notes: list[str] = Field(min_length=1)
    next_steps: list[str] = Field(min_length=1)
    does_not_execute: bool = True
    does_not_call_llm: bool = True
    does_not_use_network: bool = True
    replaces_master_orchestrator: bool = False
    requires_human_review: bool = True

    @property
    def ready_for_execution(self) -> bool:
        """Return False because this is not an execution runtime."""

        return False


def build_campaign_execution_plan(
    task_description: str,
    *,
    provided_inputs: list[str] | None = None,
) -> CampaignExecutionPlan:
    """Build a review-only campaign plan from a task description."""

    route = route_campaign(task_description)
    preconditions = evaluate_campaign_preconditions(
        route.recommended_campaign,
        provided_inputs=provided_inputs,
    )
    next_steps = [
        "review missing preconditions",
        "open related docs",
        "select owner skill manually",
        "run focused tests before changing code",
    ]
    if preconditions.ready_for_planning:
        next_steps.insert(0, "confirm campaign scope with human reviewer")
    return CampaignExecutionPlan(
        task_description=task_description,
        campaign_id=route.recommended_campaign,
        recommended_skill=route.recommended_skill,
        confidence=route.confidence,
        precondition_report=preconditions,
        expected_outputs=[
            "campaign recommendation",
            "skill handoff",
            "precondition report",
            "human review checklist",
        ],
        safety_notes=[
            "does not execute skills",
            "does not call an LLM",
            "does not use the network",
            "does not replace master orchestrator",
        ],
        next_steps=next_steps,
    )


def render_campaign_execution_plan(plan: CampaignExecutionPlan) -> str:
    """Render the execution plan as Markdown."""

    return "\n".join(
        [
            f"# Campaign Execution Plan: {plan.campaign_id}",
            "",
            f"- Recommended skill: `{plan.recommended_skill}`",
            f"- Confidence: `{plan.confidence:.2f}`",
            f"- Ready for execution: `{str(plan.ready_for_execution).lower()}`",
            f"- Does not execute: `{str(plan.does_not_execute).lower()}`",
            f"- Does not call LLM: `{str(plan.does_not_call_llm).lower()}`",
            f"- Does not use network: `{str(plan.does_not_use_network).lower()}`",
            "- Replaces master orchestrator: "
            f"`{str(plan.replaces_master_orchestrator).lower()}`",
            "",
            "## Next Steps",
            "",
            *[f"- {step}" for step in plan.next_steps],
        ]
    ) + "\n"
