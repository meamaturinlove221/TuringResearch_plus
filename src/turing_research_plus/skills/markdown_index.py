"""Markdown export helpers for skill routing."""

from __future__ import annotations

from turing_research_plus.skills.models import SkillRegistryEntry, SkillRoute


def render_routing_table(routes: list[SkillRoute]) -> str:
    """Render skill routes as Markdown."""

    lines = [
        "# TuringResearch Skill Routing Table",
        "",
        "| Category | Recommended skill | Ranked skills | Lane | Contracts |",
        "| --- | --- | --- | --- | --- |",
    ]
    for route in routes:
        lines.append(
            "| "
            f"{route.category} | "
            f"`{route.recommended_skill}` | "
            f"{', '.join(f'`{skill}`' for skill in route.ranked_skills)} | "
            f"`{route.related_lane}` | "
            f"{', '.join(f'`{contract}`' for contract in route.related_contracts)} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_registry_summary(entries: list[SkillRegistryEntry]) -> str:
    """Render a compact skill registry summary."""

    lines = [
        "# TuringResearch Skill Registry Summary",
        "",
        "| Skill | Status | Path | Release target |",
        "| --- | --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            f"| `{entry.skill_name}` | `{entry.status}` | `{entry.path}` | "
            f"`{entry.release_target}` |"
        )
    lines.append("")
    return "\n".join(lines)
