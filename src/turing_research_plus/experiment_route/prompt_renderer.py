"""Render controller prompt drafts from route specs."""

from __future__ import annotations

from turing_research_plus.experiment_route.models import ControllerPromptDraft, ExperimentRouteSpec


def render_controller_prompt(route: ExperimentRouteSpec) -> ControllerPromptDraft:
    """Render a conservative controller prompt draft without execution claims."""

    lines = [
        f"# Controller Prompt Draft: {route.route_id}",
        "",
        "This prompt is a planning artifact. It does not execute VGGT, Modal, or any backend.",
        "",
        f"Goal: {route.goal}",
        "",
        "Required boundaries:",
    ]
    lines.extend(f"- {item}" for item in route.forbidden_actions)
    lines.extend(["", "Route stages:"])
    for stage in route.stages:
        lines.append(f"- {stage.id}: {stage.name} -> gates: {', '.join(stage.hard_gates)}")
    lines.extend(["", "Final states:"])
    lines.extend(f"- {state}" for state in route.final_states)
    return ControllerPromptDraft(
        route_id=route.route_id,
        title=f"Controller Prompt Draft: {route.route_id}",
        status=route.status,
        body="\n".join(lines) + "\n",
        warnings=[
            "planned route only",
            "requires-real-experiment",
            "not executed by TuringResearch",
        ],
    )
