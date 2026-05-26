"""Markdown rendering for fake campaign execution traces."""

from __future__ import annotations

from turing_research_plus.campaigns.execution_trace import CampaignExecutionTrace


def render_campaign_execution_trace(trace: CampaignExecutionTrace) -> str:
    """Render a campaign execution trace as Markdown."""

    lines = [
        f"# Campaign Execution Trace: {trace.campaign_id}",
        "",
        f"- Trace id: `{trace.trace_id}`",
        f"- Recommended skill: `{trace.recommended_skill}`",
        f"- Confidence: `{trace.confidence:.2f}`",
        f"- Fake trace: `{str(trace.fake_trace).lower()}`",
        f"- Ready for execution: `{str(trace.ready_for_execution).lower()}`",
        f"- Does not execute: `{str(trace.does_not_execute).lower()}`",
        f"- Does not call LLM: `{str(trace.does_not_call_llm).lower()}`",
        f"- Does not use network: `{str(trace.does_not_use_network).lower()}`",
        "- Does not mutate Evidence Ledger: "
        f"`{str(trace.does_not_mutate_evidence_ledger).lower()}`",
        "",
        "## Missing Preconditions",
        "",
    ]
    lines.extend([f"- {item}" for item in trace.missing_preconditions] or ["- none"])
    lines.extend(
        [
            "",
            "## Trace Steps",
            "",
            "| Step | Status | Executed | Tool call |",
            "| --- | --- | --- | --- |",
        ]
    )
    for step in trace.steps:
        lines.append(
            f"| `{step.step_id}` | `{step.status}` | "
            f"`{str(step.executed).lower()}` | "
            f"`{str(step.called_tool).lower()}` |"
        )
    lines.extend(["", "## Step Details", ""])
    for step in trace.steps:
        lines.extend(
            [
                f"### {step.label}",
                "",
                step.description,
                "",
                "Safety:",
                "",
                *[f"- {note}" for note in step.safety_notes],
                "",
            ]
        )
    lines.extend(
        [
            "",
            "## Proposed Outputs",
            "",
            *[f"- {item}" for item in trace.proposed_outputs],
            "",
            "## Safety Notes",
            "",
            *[f"- {item}" for item in trace.safety_notes],
        ]
    )
    return "\n".join(lines) + "\n"
