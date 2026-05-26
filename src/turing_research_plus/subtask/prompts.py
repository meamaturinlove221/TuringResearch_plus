"""Role prompt rendering for single-window subtask simulation."""

from __future__ import annotations

import json

from turing_research_plus.subtask.models import SubtaskSpec, TaskProfile


def render_role_prompt(spec: SubtaskSpec, profile: TaskProfile) -> str:
    """Render a deterministic role prompt for manual Codex execution."""

    lines = [
        f"# TaskProfile: {profile.name}",
        "",
        f"Role: {profile.role}",
        f"Goal: {profile.goal}",
        f"Reasoning style: {profile.reasoning_style}",
        f"Allowed tools: {', '.join(profile.allowed_tools) if profile.allowed_tools else 'none'}",
        f"Quality gate: {profile.quality_gate or 'none'}",
        "",
        f"## Subtask: {spec.subtask_id}",
        spec.title,
        "",
        "## Inputs",
        json.dumps(spec.inputs, sort_keys=True, indent=2),
        "",
        "## Output Schema",
        json.dumps(profile.output_schema, sort_keys=True, indent=2),
    ]
    return "\n".join(lines).strip() + "\n"
